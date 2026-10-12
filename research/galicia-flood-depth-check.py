# Run after galicia-jrc-acquire.py: uv run --with rasterio python research/galicia-flood-depth-check.py
import json,pathlib,numpy as np,rasterio
from rasterio.features import geometry_mask
from rasterio.warp import reproject,Resampling
from rasterio.windows import Window
r=pathlib.Path(__file__).resolve().parents[1];o=r/'data/raw/public/galicia-flood-depth-audit'
gj=json.loads(next((r/'data/raw/public').glob('galicia-boundary-*.geojson')).read_text());geom=[f['geometry'] for f in gj['features']] if gj.get('type')=='FeatureCollection' else [gj['geometry'] if gj.get('type')=='Feature' else gj]
p=next((r/'data/raw/public/galicia-flood').glob('*historical*.tif'))
with rasterio.open(p) as d:
 a=d.read(1);tr=d.transform;crs=d.crs;shape=a.shape;inside=geometry_mask(geom,out_shape=shape,transform=tr,invert=True)
 fields={}
 for name,fn in [('jrc_positive','galicia-bbox-Europe_RP100_filled_depth.tif'),('jrc_water','galicia-bbox-Europe_permanent_water_bodies.tif'),('jrc_spurious','galicia-bbox-Europe_spurious_depth_areas.tif')]:
  with rasterio.open(o/fn) as j:
   b=j.read(1);dest=np.zeros(shape,dtype='float32');reproject((b>0).astype('float32'),dest,src_transform=j.transform,src_crs=j.crs,dst_transform=tr,dst_crs=crs,resampling=Resampling.average);fields[name]=dest
  print(name,float(dest.max()))
 result={'scope':'Galicia boundary rasterized using Aqueduct pixel-centre rule; fractions below are pixel counts not area-weighted. JRC absent positive footprint is not a verified dry classification.','source_stats':[],'groups':[]}
 for f in sorted((r/'data/raw/public/galicia-flood').glob('galicia-bbox-inunriver*.tif')):
  with rasterio.open(f) as q:b=q.read(1);v=b[inside & (b>=0)];result['source_stats'].append({'file':f.name,'valid':int(v.size),'positive':int((v>0).sum()),'tiny_0_to_0p1':int(((v>0)&(v<=.1)).sum()),'greater_0p1':int((v>.1).sum()),'greater_0p5':int((v>.5).sum()),'greater_1':int((v>1).sum()),'scales':list(q.scales),'offsets':list(q.offsets)})
 for label,mask in [('0_to_0p1',(a>0)&(a<=.1)),('above_0p1',a>.1),('exact_0p0111363186',a==np.float32(.011136318556964397)),('exact_0p020153869',a==np.float32(.020153868943452835))]:
  mask &= inside;c=int(mask.sum());g={'group':label,'count':c}
  for k,v in fields.items():g[k+'_any_cells']=int(((v>0)&mask).sum());g[k+'_mean_footprint_fraction']=float(v[mask].mean()) if c else None
  result['groups'].append(g)
 # Confirm exact values in original remote pixels, with no reprojection.
 ix=np.argwhere(inside&(a>0)&(a<.1));idx=[ix[0],ix[len(ix)//2],ix[-1]];coords=[rasterio.transform.xy(tr,int(y),int(x)) for y,x in idx]
 try:
  with rasterio.Env(GDAL_HTTP_TIMEOUT='20',GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR'):
   with rasterio.open('https://aqueduct.wridata.org/AqueductFloods20/inunriver_historical_000000000WATCH_1980_rp00100.tif') as rem:
    vals=[float(v[0]) for v in rem.sample(coords)];result['remote_checks']=[dict(lonlat=list(pt),local=float(a[y,x]),remote=val,exact_match=bool(a[y,x]==val)) for (y,x),pt,val in zip(idx,coords,vals)]
 except Exception as e:result['remote_error']=str(e)
(o/'depth-statistics.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
