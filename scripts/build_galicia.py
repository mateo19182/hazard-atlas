# /// script
# dependencies = ["xarray==2026.4.0", "h5netcdf", "h5py", "shapely", "pyproj", "numpy", "matplotlib", "rasterio"]
# ///
"""Build exploratory Galicia 10 km climate and river-flood comparisons."""
from pathlib import Path
import csv, hashlib, json, math, warnings
warnings.filterwarnings("ignore", message="All-NaN slice encountered", category=RuntimeWarning)
import numpy as np
import xarray as xr
from shapely.geometry import shape, box, mapping
from shapely.ops import transform
from shapely.strtree import STRtree
from pyproj import Transformer
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'data/derived/galicia';OUT.mkdir(parents=True,exist_ok=True)
manifest=json.loads((ROOT/'data/manifest.json').read_text())
inputs=[]
def source(sid):
 e=next(e for e in manifest if e['source_id']==sid)
 p=ROOT/e['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']
 inputs.append({'path':e['path'],'sha256':e['sha256'],'source_id':sid})
 return p
project=Transformer.from_crs(4326,3035,always_xy=True).transform
unproject=Transformer.from_crs(3035,4326,always_xy=True).transform
boundary_json=json.loads(source('galicia-boundary').read_text())
if boundary_json['type']=='FeatureCollection': geom=shape(boundary_json['features'][0]['geometry'])
elif boundary_json['type']=='Feature': geom=shape(boundary_json['geometry'])
else: geom=shape(boundary_json)
region=transform(project,geom)
assert region.is_valid and 28000<region.area/1e6<31000
xmin,ymin,xmax,ymax=region.bounds
grid=[];ids=[]
for x in range(math.floor(xmin/10000)*10000,math.ceil(xmax/10000)*10000,10000):
 for y in range(math.floor(ymin/10000)*10000,math.ceil(ymax/10000)*10000,10000):
  g=box(x,y,x+10000,y+10000).intersection(region)
  if g.area>1: grid.append(g);ids.append(f'E{x//10000}_N{y//10000}')
areas=np.array([g.area for g in grid])
assert abs(areas.sum()-region.area)/region.area<1e-9

# Weight native cells by their actual overlap with each clipped 10 km cell.
def weights(polygons):
 tree=STRtree(polygons); result=[]
 for target in grid:
  idx=tree.query(target,predicate='intersects')
  a=np.array([polygons[i].intersection(target).area for i in idx])
  keep=a>0;result.append((np.asarray(idx)[keep],a[keep]))
 return result

def aggregate(arr,ws):
 # Leading dimensions are model and period; final dimension is source cell.
 values=np.full(arr.shape[:-1]+(len(grid),),np.nan)
 coverage=np.zeros_like(values)
 for j,(idx,w) in enumerate(ws):
  if not len(idx):continue
  a=arr[...,idx];valid=np.isfinite(a);den=(valid*w).sum(axis=-1)
  coverage[...,j]=den/areas[j]
  np.divide(np.nansum(a*w,axis=-1),den,out=values[...,j],where=den>0)
  values[...,j]=np.where(coverage[...,j]>=.8,values[...,j],np.nan)
 return values,coverage

periods=['reference','near_future','medium_future']
metadata={
 'tasmaxmax':dict(label='Annual maximum temperature',unit='°C',cmap='YlOrRd',meaning='Climatological annual maximum of daily maximum temperature. A 10 km area average of source indices, not a local record temperature.'),
 'tasmaxhwdmax':dict(label='Longest heatwave',unit='days',cmap='YlOrRd',meaning='Longest spell above the local historical 90th percentile; relative heat, not absolute temperature.'),
 'prspellb1':dict(label='Longest dry spell',unit='days',cmap='YlOrBr',meaning='Longest run of days with rainfall below 1 mm. Not water availability or a full drought assessment.'),
 'prmax24':dict(label='Annual maximum daily rainfall',unit='mm',cmap='YlGnBu',meaning='Climatological annual maximum daily precipitation. Not river or surface-water flood depth.')}
records={};ensemble={}; ws=None;expected_coords=None
for var,meta in metadata.items():
 records[var]={};ensemble[var]={}
 for scenario in ['ssp245','ssp370']:
  if var=='tasmaxhwdmax' and scenario=='ssp370':continue
  sid='adaptecca-heat-ssp245' if var=='tasmaxhwdmax' else f'adaptecca-{var}-{scenario}'
  with xr.open_dataset(source(sid)) as ds:
   d=ds.sel(lat=slice(geom.bounds[1]-.1,geom.bounds[3]+.1),lon=slice(geom.bounds[0]-.1,geom.bounds[2]+.1))
   members=[str(m) for m in d.member.values if m!='average']
   lats=d.lat.values;lons=d.lon.values
   if ws is None:
    src=[transform(project,box(lon-.025,lat-.025,lon+.025,lat+.025)) for lat in lats for lon in lons]
    ws=weights(src);expected_coords=(lats,lons)
   else:
    assert np.array_equal(lats,expected_coords[0]) and np.array_equal(lons,expected_coords[1])
   raw=d[var].sel(member=members,time_filter='year',period=periods).transpose('member','period','lat','lon').values.reshape(len(members),3,-1)
   v,c=aggregate(raw,ws)
   assert np.nanmin(c)>=0 and np.nanmax(c)<1.000001
   ensemble[var][scenario]=v
   delta=v[:,2]-v[:,0]
   with np.errstate(all='ignore'):
    rec={'baseline':np.nanmedian(v[:,0],axis=0),'near':np.nanmedian(v[:,1],axis=0),'future':np.nanmedian(v[:,2],axis=0),'change':np.nanmedian(delta,axis=0),'spread':np.nanpercentile(v[:,2],90,axis=0)-np.nanpercentile(v[:,2],10,axis=0),'p10':np.nanpercentile(v[:,2],10,axis=0),'p90':np.nanpercentile(v[:,2],90,axis=0),'coverage':np.min(c,axis=(0,1)), 'model_count':np.isfinite(v[:,2]).sum(axis=0)}
   records[var][scenario]=rec
   meta.update(baseline_label='Historical model baseline · 1971–2000',near_label='Near-term model window · 2011–2040',future_label='Mid-century · 2041–2070',members=members)
   print(var,scenario,'cells',int(np.isfinite(rec['future']).sum()),flush=True)

# Flood data are optional, supplied by the independent source-access audit.
flood_dir=ROOT/'data/raw/public/galicia-flood'
files=sorted(flood_dir.glob('galicia-bbox-inunriver*.tif'))
if len(files)>=6:
 import rasterio
 flood=[];flood10=[];flood_names=[];fws=None
 for path in files:
  inputs.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'processing':'See research/galicia-flood-acquire.py'})
  with rasterio.open(path) as r:
   data=r.read(1,masked=True).filled(np.nan)
   if fws is None:
    fps=[]
    for row in range(r.height):
     for col in range(r.width):
      left,top=r.transform*(col,row);right,bottom=r.transform*(col+1,row+1)
      fps.append(transform(project,box(left,bottom,right,top)))
    fws=weights(fps);reference_transform=r.transform;reference_shape=data.shape;reference_valid=np.isfinite(data)
   assert r.transform==reference_transform and data.shape==reference_shape
   assert np.array_equal(np.isfinite(data),reference_valid), 'Flood model coverage changed; use shared domain before differencing'
   wet=np.where(np.isfinite(data),(data>0).astype(float)*100,np.nan)
   vals,cov=aggregate(wet.reshape(1,-1),fws)
   flood.append(vals[0]);flood_names.append(path.name)
   wet10=np.where(np.isfinite(data),(data>.1).astype(float)*100,np.nan)
   vals10,_=aggregate(wet10.reshape(1,-1),fws);flood10.append(vals10[0])
 base_idx=next(i for i,n in enumerate(flood_names) if 'historical' in n)
 future_idx=[i for i,n in enumerate(flood_names) if '2050' in n]
 assert len(future_idx)==5
 for key,series,threshold in [('river_flood',flood,0),('river_flood_10cm',flood10,.1)]:
  base=series[base_idx];fut=np.array([series[i] for i in future_idx]);delta=fut-base
  records[key]={'rcp45':{'baseline':base,'near':np.full_like(base,np.nan),'future':np.nanmedian(fut,axis=0),'change':np.nanmedian(delta,axis=0),'spread':np.nanpercentile(fut,90,axis=0)-np.nanpercentile(fut,10,axis=0),'p10':np.nanpercentile(fut,10,axis=0),'p90':np.nanpercentile(fut,90,axis=0),'coverage':cov[0],'model_count':np.isfinite(fut).sum(axis=0)}}
  metadata[key]=dict(label=f'River flood footprint · depth >{threshold:g} m',unit='% model-covered area',cmap='Blues',meaning=f'Area with modelled depth >{threshold:g} m for a 100-year river flood, divided by valid mapped area. No flood defences. Compare both depth thresholds: tiny positive values can dominate the >0 m footprint. Zero does not rule out small streams, coastal or rainfall-driven flooding.',baseline_label='River model baseline · 1960–1999',near_label='Not available',future_label='2050 label · 2030–2069',members=[flood_names[i] for i in future_idx])

def clean(a):
 a=np.asarray(a);return [None if not np.isfinite(v) else round(float(v),4) for v in a]
features=[]
for i,g in enumerate(grid):
 props={'id':ids[i],'area_km2':round(areas[i]/1e6,4)}
 features.append({'type':'Feature','geometry':mapping(transform(unproject,g)),'properties':props})
(OUT/'grid.geojson').write_text(json.dumps({'type':'FeatureCollection','features':features}))
values={var:{sc:{k:clean(a) for k,a in rec.items()} for sc,rec in scenarios.items()} for var,scenarios in records.items()}
payload={'metadata':metadata,'values':values,'cells':[f['properties'] for f in features]}
(OUT/'indicators.json').write_text(json.dumps(payload,allow_nan=False))
with (OUT/'indicators.csv').open('w') as f:
 writer=csv.writer(f);writer.writerow(['cell_id','area_km2','indicator','scenario','baseline','near','future','change','p10','p90','spread','coverage','model_count'])
 for var,scs in values.items():
  for sc,rec in scs.items():
   for i,c in enumerate(payload['cells']):writer.writerow([c['id'],c['area_km2'],var,sc]+[rec[k][i] for k in ['baseline','near','future','change','p10','p90','spread','coverage','model_count']])
np.savez_compressed(OUT/'climate-member-values.npz',**{v+'_'+s:a for v,ss in ensemble.items() for s,a in ss.items()})
# Static figure with physical units and no combined hazard score.
fig,axs=plt.subplots(2,2,figsize=(11,11));fig.patch.set_facecolor('#f7f8f5')
for ax,var in zip(axs.flat,metadata):
 if var=='river_flood':break
 vals=records[var]['ssp245']['future']; patches=[];colors=[]
 for g,v in zip(grid,vals):
  for poly in ([g] if g.geom_type=='Polygon' else g.geoms):
   if poly.geom_type!='Polygon':continue
   patches.append(Polygon(np.asarray(poly.exterior.coords)/1000,closed=True));colors.append(v)
 palette=plt.get_cmap(metadata[var]['cmap']).copy();palette.set_bad('#d4dad7')
 pc=PatchCollection(patches,cmap=palette,edgecolors='#ffffff',linewidths=.15)
 pc.set_array(np.ma.masked_invalid(colors));ax.add_collection(pc);ax.autoscale();ax.set_aspect('equal');ax.axis('off');ax.set_title(metadata[var]['label'],fontsize=12)
 cb=fig.colorbar(pc,ax=ax,shrink=.66);cb.set_label(metadata[var]['unit'])
fig.suptitle('Galicia · 10 km exploratory climate grid\n2041–2070 · SSP2-4.5 · median across 11 models',fontsize=16)
fig.text(.05,.025,'AdapteCCa / AEMET / CSIC · Boundary: Eurostat GISCO\nArea-weighted source indices; cells with <80% valid coverage are grey. No overall safety score.',fontsize=9)
fig.savefig(OUT/'galicia-climate.png',dpi=160,bbox_inches='tight');plt.close(fig)
summary={var:{sc:{'mapped_cells':int(np.isfinite(r['future']).sum()),'median_cell_change':float(np.nanmedian(r['change'])),'future_cell_range':[float(np.nanmin(r['future'])),float(np.nanmax(r['future']))]} for sc,r in scs.items()} for var,scs in records.items()}
provenance={'grid_crs':'EPSG:3035','cell_side_m':10000,'grid_origin':[0,0],'boundary':'GISCO ES11 2024 1:1 million','cells':len(grid),'area_km2':float(areas.sum()/1e6),'minimum_valid_area_fraction':.8,'method':'Area-overlap weighted mean per source model and period, then ensemble median; climate changes paired by model; river changes compare each future forcing against one WATCH baseline; P90 minus P10 model spread. Source average member excluded.','inputs':inputs,'summary':summary,'script':'scripts/build_galicia.py'}
(OUT/'provenance.json').write_text(json.dumps(provenance,indent=2))
# SVG geometry for a self-contained interactive research artifact.
scale=650/(xmax-xmin);height=(ymax-ymin)*scale
paths=[]
for g in grid:
 parts=[]
 for poly in ([g] if g.geom_type=='Polygon' else g.geoms):
  if poly.geom_type!='Polygon':continue
  for ring in [poly.exterior,*poly.interiors]:
   xy=[((x-xmin)*scale,(ymax-y)*scale) for x,y in ring.coords]
   parts.append('M'+' L'.join(f'{x:.2f},{y:.2f}' for x,y in xy)+' Z')
 paths.append(' '.join(parts))
payload['paths']=paths;payload['height']=height
payload['cities']=[]
for name,lon,lat in [('A Coruña',-8.4115,43.3623),('Lugo',-7.556,43.01),('Santiago',-8.5448,42.8782),('Ourense',-7.8639,42.3358),('Vigo',-8.7207,42.2406)]:
 x,y=project(lon,lat);payload['cities'].append([name,(x-xmin)*scale,(ymax-y)*scale])
template=(ROOT/'scripts/galicia-report-template.html').read_text()
(OUT/'galicia.html').write_text(template.replace('__DATA__',json.dumps(payload,allow_nan=False)))
print(json.dumps(provenance['summary'],indent=2));print('Cells',len(grid),'area km2',areas.sum()/1e6)
