# Reproduce access samples: uv run --with rasterio --with pyproj python research/galicia-flood-acquire.py
import json,pathlib,urllib.request,datetime,hashlib
import rasterio,numpy as np
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds
from pyproj import Transformer
root=pathlib.Path(__file__).resolve().parents[1]; out=root/'data/raw/public/galicia-flood';out.mkdir(parents=True,exist_ok=True)
records=[]; checks=[]
def record(p,url,processing=None):
 b=p.read_bytes();records.append(dict(path=str(p.relative_to(root)),url=url,sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),acquired_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),processing=processing))
def crop(url,name,bounds,crs):
 with rasterio.Env(GDAL_HTTP_TIMEOUT='25',GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR'):
  with rasterio.open(url) as ds:
   b=transform_bounds(crs,ds.crs,*bounds,densify_pts=21)
   w=from_bounds(*b,ds.transform).round_offsets().round_lengths()
   arr=ds.read(1,window=w);p=out/name;pr=ds.profile;pr.update(width=arr.shape[1],height=arr.shape[0],transform=ds.window_transform(w),compress='deflate')
   with rasterio.open(p,'w',**pr) as dst:dst.write(arr,1)
   valid=arr[np.isfinite(arr)&(arr!=ds.nodata)]
   ck=dict(path=str(p.relative_to(root)),url=url,crs=str(ds.crs),resolution=list(ds.res),nodata=ds.nodata,window=dict(w.todict()),shape=list(arr.shape),requested_bounds=list(bounds),requested_crs=crs,valid_count=int(valid.size),positive_count=int((valid>0).sum()),zero_count=int((valid==0).sum()),negative_count=int((valid<0).sum()),maximum=float(valid.max()) if valid.size else None)
   checks.append(ck);record(p,url,'HTTP range crop with rasterio; see galicia-flood-access-checks.json');print(json.dumps(ck),flush=True)
base='https://minio.dive.edito.eu/project-coclico/coclico-stac-edito/cfhp_all/items/UNDEFENDED_MAPS/100/'
x,y=Transformer.from_crs(4326,3035,always_xy=True).transform(-8.85,42.5)
for key in ['None/2010','SSP245/2050']:
 try:
  u=base+key+'.json';b=urllib.request.urlopen(u,timeout=25).read();p=out/('coclico-'+key.replace('/','-')+'.json');p.write_bytes(b);record(p,u)
  d=json.loads(b)
  for a in d['assets'].values():
   bb=a.get('proj:bbox')
   if bb and bb[0]<x<bb[2] and bb[1]<y<bb[3]:
    crop(a['href'],'coclico-rias-baixas-'+key.replace('/','-')+'-rp100-undefended.tif',(x-15000,y-15000,x+15000,y+15000),'EPSG:3035')
 except Exception as e:checks.append({'source':'coclico '+key,'error':str(e)});print('ERROR',str(e),flush=True)
for f in ['inunriver_historical_000000000WATCH_1980_rp00100.tif','inunriver_rcp4p5_00000NorESM1-M_2050_rp00100.tif','inunriver_rcp4p5_0000GFDL-ESM2M_2050_rp00100.tif','inunriver_rcp4p5_0000HadGEM2-ES_2050_rp00100.tif','inunriver_rcp4p5_00IPSL-CM5A-LR_2050_rp00100.tif','inunriver_rcp4p5_MIROC-ESM-CHEM_2050_rp00100.tif']:
 try:crop('https://aqueduct.wridata.org/AqueductFloods20/'+f,'galicia-bbox-'+f,(-9.35,41.75,-6.7,43.85),'EPSG:4326')
 except Exception as e:checks.append({'source':f,'error':str(e)});print('ERROR',str(e),flush=True)
p=out/'galicia-flood-access-checks.json';p.write_text(json.dumps(checks,indent=2)+'\n');record(p,None,'Locally generated access evidence')
(root/'research/galicia-flood-artifacts.json').write_text(json.dumps({'artifacts':records},indent=2)+'\n')
