# Run with uv run --with rasterio python research/galicia-jrc-acquire.py
import rasterio,numpy as np,json,pathlib,datetime,hashlib,urllib.request
from rasterio.windows import from_bounds
root=pathlib.Path(__file__).resolve().parents[1];out=root/'data/raw/public/galicia-flood-depth-audit';out.mkdir(parents=True,exist_ok=True)
records=[];checks=[];base='https://jeodpp.jrc.ec.europa.eu/ftp/jrc-opendata/CEMS-EFAS/flood_hazard/'
def rec(p,u):
 b=p.read_bytes();records.append(dict(path=str(p.relative_to(root)),url=u,sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),acquired_at=datetime.datetime.now(datetime.timezone.utc).isoformat()))
for f in ['README.txt','CHANGELOG.txt','copyright.txt']:
 p=out/f;p.write_bytes(urllib.request.urlopen(base+f,timeout=25).read());rec(p,base+f)
for f in ['Europe_RP100_filled_depth.tif','Europe_permanent_water_bodies.tif','Europe_spurious_depth_areas.tif']:
 try:
  with rasterio.Env(GDAL_HTTP_TIMEOUT='25',GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR'):
   with rasterio.open(base+f) as ds:
    w=from_bounds(-9.35,41.75,-6.7,43.85,ds.transform).round_offsets().round_lengths();a=ds.read(1,window=w)
    p=out/('galicia-bbox-'+f);pr=ds.profile;pr.update(width=a.shape[1],height=a.shape[0],transform=ds.window_transform(w),compress='deflate')
    with rasterio.open(p,'w',**pr) as d:d.write(a,1)
    rec(p,base+f);v=a[np.isfinite(a)&(a!=ds.nodata)];info=dict(file=f,crs=str(ds.crs),resolution=list(ds.res),nodata=ds.nodata,scales=ds.scales,offsets=ds.offsets,shape=a.shape,valid=int(v.size),positive=int((v>0).sum()),zero=int((v==0).sum()),maximum=float(v.max()) if v.size else None,unique_preview=np.unique(v)[:20].tolist());checks.append(info);print(json.dumps(info),flush=True)
 except Exception as e:checks.append({'file':f,'error':str(e)});print(str(e),flush=True)
p=out/'jrc-access-check.json';p.write_text(json.dumps(checks,indent=2)+'\n');rec(p,None)
(root/'research/galicia-flood-depth-artifacts.json').write_text(json.dumps({'artifacts':records},indent=2)+'\n')
