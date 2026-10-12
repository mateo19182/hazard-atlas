# /// script
# dependencies = ["numpy", "rasterio", "shapely", "pyproj"]
# ///
"""Aggregate complete single-model fire-weather periods to the Galicia pilot grid.

Run with uv run scripts/build_fire_highres.py. Requires all 40 annual crops.
Writes only optional fire-highres.json and its own provenance, never main outputs.
"""
from pathlib import Path
import hashlib,json,re,calendar
import numpy as np
import rasterio
from shapely.geometry import shape,box
from shapely.ops import transform
from shapely.strtree import STRtree
from pyproj import Transformer

ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw/public/galicia-fire9km-access'
OUT=ROOT/'data/derived/galicia'
PERIODS={'baseline':range(1995,2015),'future':range(2041,2061)}
MODEL='MRI-ESM2-0'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def clean(a):return [None if not np.isfinite(v) else round(float(v),4) for v in a]

def main():
    gridpath=OUT/'grid.geojson'
    griddata=json.loads(gridpath.read_text())
    cells=[f['properties'] for f in griddata['features']]
    project=Transformer.from_crs(4326,3035,always_xy=True).transform
    targets=[transform(project,shape(f['geometry'])) for f in griddata['features']]
    areas=np.array([g.area for g in targets])
    files={};missing=[]
    for period,years in PERIODS.items():
        for year in years:
            candidates=[]
            for p in RAW.glob('galicia-bbox-*.tif'):
                if re.search(rf'(?:_|\b){year}(?:_|\b)',p.name) and MODEL in p.name:
                    if period=='future' and 'ssp245' not in p.name.lower():continue
                    if period=='baseline' and not any(s in p.name.lower() for s in ['historical','histo']):continue
                    candidates.append(p)
            if len(candidates)!=1:missing.append((period,year,len(candidates)))
            else:files[period,year]=candidates[0]
    if missing:
        raise SystemExit('Complete 20-year periods required; missing/ambiguous year files: '+str(missing))
    annual={'fwi_mean':{},'fwi_days_gt30':{}};inputs=[];signature=None;native=None
    for (period,year),path in sorted(files.items()):
        with rasterio.open(path) as ds:
            sig=(ds.height,ds.width,tuple(ds.transform))
            if signature is None:
                signature=sig
                if abs(ds.transform.b)>1e-12 or abs(ds.transform.d)>1e-12:raise ValueError('Rotated grid unsupported')
                native=[]
                for row in range(ds.height):
                    for col in range(ds.width):
                        x0,y0=ds.transform*(col,row);x1,y1=ds.transform*(col+1,row+1)
                        native.append(transform(project,box(min(x0,x1),min(y0,y1),max(x0,x1),max(y0,y1))))
            if sig!=signature:raise ValueError('Annual native grids differ: '+str(path))
            if ds.count!=365+calendar.isleap(year):raise ValueError('Daily band count does not match year length: '+str(path))
            day_count=ds.count
            if ds.crs and ds.crs.to_epsg()!=4326:raise ValueError('Unexpected crop CRS: '+str(ds.crs))
            arr=ds.read(masked=True).filled(np.nan).astype('float64').reshape(day_count,-1)
            valid=np.isfinite(arr).all(axis=0)
            if np.any(arr[np.isfinite(arr)]<0):raise ValueError('Negative FWI requires investigation')
            mean=np.full(arr.shape[1],np.nan);days=mean.copy()
            mean[valid]=arr[:,valid].mean(axis=0)
            days[valid]=(arr[:,valid]>30).sum(axis=0)
            annual['fwi_mean'][period,year]=mean
            annual['fwi_days_gt30'][period,year]=days
        inputs.append({'path':str(path.relative_to(ROOT)),'sha256':sha(path),'period':period,'year':year,'daily_bands':day_count})
    tree=STRtree(native);weights=[]
    for target in targets:
        ids=tree.query(target,predicate='intersects')
        w=np.array([native[i].intersection(target).area for i in ids]);keep=w>0
        weights.append((np.asarray(ids)[keep],w[keep]))
    metadata={};values={};summaries={}
    for name,byyear in annual.items():
        b=np.stack([byyear['baseline',y] for y in PERIODS['baseline']])
        f=np.stack([byyear['future',y] for y in PERIODS['future']])
        # The same native cells must contain every daily value in all 40 annual files.
        shared=np.isfinite(b).all(axis=0)&np.isfinite(f).all(axis=0)
        bm=np.full(b.shape[1],np.nan);fm=bm.copy()
        bm[shared]=b[:,shared].mean(axis=0);fm[shared]=f[:,shared].mean(axis=0)
        baseline=np.full(len(cells),np.nan);future=baseline.copy();coverage=np.zeros(len(cells))
        for i,(idx,w) in enumerate(weights):
            ok=shared[idx];den=w[ok].sum();coverage[i]=den/areas[i]
            if den>0 and coverage[i]>=.8:
                baseline[i]=np.dot(bm[idx[ok]],w[ok])/den
                future[i]=np.dot(fm[idx[ok]],w[ok])/den
        if np.any(coverage>1+1e-6):raise ValueError('Source overlap exceeds target area')
        nulls=[None]*len(cells)
        values[name]={'ssp245':{'baseline':clean(baseline),'near':nulls,'future':clean(future),'change':clean(future-baseline),'spread':nulls,'p10':nulls,'p90':nulls,'coverage':clean(coverage),'model_count':[1 if np.isfinite(x) else 0 for x in future]}}
        label='Annual mean fire-weather index' if name=='fwi_mean' else 'Days with fire-weather index >30'
        unit='FWI' if name=='fwi_mean' else 'days/year'
        metadata[name]={'future_stat_label':'Future value · one model','processing_note':'Area-overlap aggregation of 0.0703135° source cells; MRI-ESM2-0 only.','change_label':'Change within MRI-ESM2-0','label':label,'unit':unit,'cmap':'YlOrRd','baseline_label':'Historical model baseline · 1995–2014','future_label':'Mid-century · 2041–2060','near_label':'Not available','members':[MODEL],'ensemble_note':'One climate model, MRI-ESM2-0. Model spread unavailable.','available_modes':['future','baseline','change','coverage'],'meaning':'All-season meteorological fire pressure from all daily bands in each annual file, averaged across 20 complete years and area-weighted to 10 km. Not ignition probability, burned area or property risk.','source_url':'https://doi.org/10.5281/zenodo.19792063','source_grid':'0.0703135°; approximately 6 by 8 km in Galicia','detail_note':'Single-model SSP2-4.5 experiment; Annual files contain 365 or 366 daily bands; individual band dates are not stored. FWI >30 is an explicit indicator threshold.'}
        valid=np.isfinite(future)
        summaries[name]={'valid_cells':int(valid.sum()),'shared_area_fraction':float(np.sum(coverage*areas)/areas.sum()),'regional_baseline_over_valid_area_in_retained_target_cells':float(np.dot(baseline[valid],areas[valid]*coverage[valid])/(areas[valid]*coverage[valid]).sum()) if valid.any() else None,'regional_future_over_valid_area_in_retained_target_cells':float(np.dot(future[valid],areas[valid]*coverage[valid])/(areas[valid]*coverage[valid]).sum()) if valid.any() else None}
    payload={'metadata':metadata,'values':values,'cells':cells}
    provenance={'annual_file_inventory_sha256':sha(RAW/'annual-file-inventory.json') if (RAW/'annual-file-inventory.json').exists() else None,'grid_sha256':sha(gridpath),'source_url':'https://doi.org/10.5281/zenodo.19792063','license':'CC-BY-4.0','model':MODEL,'scenario':'SSP2-4.5','reference_years':[1995,2014],'future_years':[2041,2060],'source_crs_interpretation':'EPSG:4326 assumed from published geographic-degree coordinates; original TIFF CRS tag absent','calendar_limit':'Actual 365 or 366 daily bands retained per annual file; individual month/day dates not stored and not assigned. Annual means weight years equally.','method':'For each annual native pixel require every daily band to be finite; compute mean FWI and count FWI strictly greater than 30. Require all 20 annual summaries in both periods on identical native pixels; average years equally. Project native pixel polygons and Galicia 10 km geometry to EPSG:3035, weight by overlap area. Require 80% shared valid area. Single model, no ensemble quantiles.','inputs':inputs,'summary':summaries,'script':'scripts/build_fire_highres.py'}
    (OUT/'fire-highres.json').write_text(json.dumps(payload,allow_nan=False))
    (OUT/'fire-highres-provenance.json').write_text(json.dumps(provenance,indent=2,allow_nan=False)+'\n')
    print(json.dumps(summaries,indent=2))
if __name__=='__main__':main()
