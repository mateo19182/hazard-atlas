# /// script
# dependencies = ["shapely", "numpy", "rasterio", "pyproj"]
# ///
"""Acquire bbox-filtered SNCZI T100 positives and compare exact areas to Aqueduct.
Run with uv run research/galicia-flood-validate.py. Cached requests are preserved.
"""
from pathlib import Path
import urllib.request, json, hashlib, datetime, collections, gzip, time, concurrent.futures
import numpy as np
import shapely
from shapely.geometry import shape,box,mapping
def transform(fn,g):return shapely.transform(g,fn,interleaved=False)
from pyproj import Transformer
import rasterio
ROOT=Path(__file__).resolve().parents[1]
RAW=ROOT/'data/raw/public/galicia-snczi';RAW.mkdir(parents=True,exist_ok=True)
OUT=ROOT/'data/derived/galicia';OUT.mkdir(parents=True,exist_ok=True)
artifacts=[]
def acquire(name,url):
 p=RAW/name
 if not p.exists():
  for attempt in range(3):
   try:
    with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'hazard-atlas research','Accept-Encoding':'gzip'}),timeout=120) as r:
     b=r.read()
     if r.headers.get('Content-Encoding')=='gzip':b=gzip.decompress(b)
    break
   except Exception:
    if attempt==2:raise
    time.sleep(2)
  j=json.loads(b);p.write_bytes(b)
 else:b=p.read_bytes();j=json.loads(b)
 artifacts.append(dict(path=str(p.relative_to(ROOT)),url=url,sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),acquired_at=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat()))
 return j
base='https://gis.miteco.gob.es/geoserver/ogc/features/v1/collections/agua:Zi_laminas_q100'
meta=acquire('collection.json',base+'?f=json')
d=acquire('t100-page-000.geojson',base+'/items?f=json&bbox=-9.35,41.75,-6.7,43.85&limit=100')
features=list(d['features']);matched=d['numberMatched']
print('cached first page',len(features),'of',matched,flush=True)
def fetch_batch(start):
 url=base+f'/items?f=json&bbox=-9.35,41.75,-6.7,43.85&limit=25&startIndex={start}'
 data=acquire(f't100-start-{start:05}.geojson',url)
 assert data['numberMatched']==matched
 print('acquired start',start,'count',len(data['features']),flush=True)
 return data['features']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 for batch in pool.map(fetch_batch,range(len(features),matched,25)):features.extend(batch)
assert len(features)==matched and len({f['id'] for f in features})==len(features)
artifacts.sort(key=lambda a:a['path'])
(ROOT/'research/galicia-snczi-artifacts.json').write_text(json.dumps({'artifacts':artifacts},indent=2)+'\n')
project=Transformer.from_crs(4326,3035,always_xy=True).transform
unproject=Transformer.from_crs(3035,4326,always_xy=True).transform
gj=json.loads((OUT/'grid.geojson').read_text());grid=[transform(project,shape(f['geometry'])) for f in gj['features']];region=shapely.union_all(grid)
invalid=0;geoms=[];inside=[]
for f in features:
 g=transform(project,shape(f['geometry']))
 if not g.is_valid:invalid+=1;g=shapely.make_valid(g)
 if g.intersects(region):
  g=g.intersection(region)
  if g.area>0:geoms.append(g);inside.append(f)
official=shapely.union_all(geoms);shapely.prepare(official)
parts_official=shapely.get_parts(official);official_tree=shapely.STRtree(parts_official)
def local_official(g):
 ix=official_tree.query(g,predicate='intersects')
 return shapely.union_all(shapely.intersection(parts_official[ix],g))
(OUT/'snczi-t100-clipped.geojson').write_text(json.dumps({'type':'FeatureCollection','features':[{'type':'Feature','geometry':mapping(transform(unproject,g)),'properties':f['properties']} for g,f in zip(geoms,inside)]}))
print('official geometries',len(geoms),'area km2',official.area/1e6,flush=True)
p=next((ROOT/'data/raw/public/galicia-flood').glob('*historical*rp00100.tif'))
with rasterio.open(p) as r:
 assert r.crs.to_epsg()==4326
 a=r.read(1,masked=True).filled(np.nan); pixels=[];depth=[]
 for row,col in np.argwhere(np.isfinite(a)):
  left,top=r.transform*(int(col),int(row));right,bottom=r.transform*(int(col)+1,int(row)+1)
  g=transform(project,box(left,bottom,right,top))
  if g.intersects(region):
   g=g.intersection(region)
   if g.area>0:pixels.append(g);depth.append(float(a[row,col]))
pixels=np.array(pixels,dtype=object);depth=np.array(depth);areas=shapely.area(pixels)
print('valid pixels',len(pixels),flush=True)
official_overlap=np.zeros(len(pixels));idx=np.where(shapely.intersects(pixels,official))[0]
for k,i in enumerate(idx):
 js=official_tree.query(pixels[i],predicate='intersects')
 official_overlap[i]=shapely.area(shapely.intersection(parts_official[js],pixels[i])).sum()
 if k%1000==0:print('official pixel overlaps',k,'of',len(idx),flush=True)
valid_area=areas.sum();official_in_valid=official_overlap.sum()
thresholds=[0,.1,.5,1];totals={}
for t in thresholds:
 wet=depth>t;aq=areas[wet].sum();intersection=official_overlap[wet].sum()
 totals[str(t)]={'aqueduct_positive_km2':float(aq/1e6),'intersection_km2':float(intersection/1e6),'official_positive_in_valid_captured_fraction':float(intersection/official_in_valid),'aqueduct_positive_overlapping_official_fraction':float(intersection/aq) if aq else None}
# Exact overlap weights. Valid mapped area is the Aqueduct denominator;
# official positive fraction uses clipped target-cell area without asserting full study coverage.
tree=shapely.STRtree(pixels);cells=[]
for f,g in zip(gj['features'],grid):
 ix=tree.query(g,predicate='intersects');parts=shapely.intersection(pixels[ix],g);w=shapely.area(parts);den=w.sum()
 op=local_official(g);oa=op.area
 ovalid=shapely.area(shapely.intersection(parts,op)).sum() if oa else 0.
 row={'id':f['properties']['id'],'area_km2':g.area/1e6,'official_positive_km2':oa/1e6,'official_positive_with_aqueduct_coverage_km2':float(ovalid/1e6),'official_positive_fraction_of_cell':oa/g.area,'official_study_coverage':'unknown','aqueduct_valid_fraction_of_cell':den/g.area,'aqueduct_coverage_at_least_80_percent':bool(den/g.area>=.8),'thresholds':{}}
 for t in thresholds:
  wet=depth[ix]>t;wa=w[wet].sum();intersection=shapely.area(shapely.intersection(parts[wet],op)).sum() if oa else 0.
  row['thresholds'][str(t)]={'aqueduct_positive_km2':float(wa/1e6),'aqueduct_positive_fraction_of_valid_area':float(wa/den) if den else None,'intersection_km2':float(intersection/1e6),'official_positive_captured_fraction':float(intersection/oa) if oa else None,'official_positive_in_valid_captured_fraction':float(intersection/ovalid) if ovalid else None}
 cells.append(row)
summary={'source':'MITECO SNCZI fluvial T100, OGC API bounded extraction','source_url':base,'aqueduct_path':str(p.relative_to(ROOT)),'aqueduct_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'grid_path':'data/derived/galicia/grid.geojson','grid_sha256':hashlib.sha256((OUT/'grid.geojson').read_bytes()).hexdigest(),'rights':'MITECO download page permits free reuse with attribution: Fuente: Ministerio para la Transición Ecológica y el Reto Demográfico.','rights_url':'https://www.miteco.gob.es/es/cartografia-y-sig/ide/descargas/agua/zi-lamina.html','crs':'EPSG:3035','method':'Exact area overlaps of official polygons and native Aqueduct pixels, clipped to GISCO Galicia boundary. Threshold comparisons use historical WATCH RP100. No overall accuracy or false-positive rate because official study coverage is unknown.','official_study_coverage':'unknown','bbox_feature_count':len(features),'features_intersecting_galicia':len(inside),'repaired_invalid_features':invalid,'galicia_area_km2':region.area/1e6,'official_positive_km2':official.area/1e6,'aqueduct_valid_km2':float(valid_area/1e6),'official_positive_with_aqueduct_coverage_km2':float(official_in_valid/1e6),'thresholds':totals,'attribute_counts':{k:dict(collections.Counter(str(f['properties'].get(k)) for f in inside)) for k in ['ciclo','fecha_geo','fecha_apro','hipotesis','precision','hidraul','organismo','demarcacio']}}
assert abs(sum(c['official_positive_km2'] for c in cells)-summary['official_positive_km2'])<.001
for t in thresholds:
 assert abs(sum(c['thresholds'][str(t)]['intersection_km2'] for c in cells)-totals[str(t)]['intersection_km2'])<.001
payload={'metadata':summary,'cells':cells};(OUT/'flood-validation.json').write_text(json.dumps(payload,indent=2,allow_nan=False)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='attribute_counts'},indent=2))
