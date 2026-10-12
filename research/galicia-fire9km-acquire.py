# /// script
# dependencies = ["rasterio", "playwright"]
# ///
"""Bounded native-grid acquisition: one model, 40 years, three concurrent crops.
Run with uv run research/galicia-fire9km-acquire.py. Install Playwright Chromium first.
Public provider UI only; ephemeral request/session data stays outside the repo.
"""
import json,pathlib,urllib.request,datetime,hashlib,concurrent.futures,time
import rasterio,numpy as np,calendar
from rasterio.windows import from_bounds
root=pathlib.Path(__file__).resolve().parents[1];out=root/'data/raw/public/galicia-fire9km-access';out.mkdir(parents=True,exist_ok=True)
# Capture unauthenticated request templates from the provider's public UI.
# They remain in a temporary directory; cookies and signed URLs are never archived.
import asyncio,tempfile
from playwright.async_api import async_playwright
session=pathlib.Path(tempfile.mkdtemp(prefix='hazard-atlas-fire-'))
async def bootstrap():
 async with async_playwright() as p:
  binaries=sorted((pathlib.Path.home()/'.cache/ms-playwright').glob('chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell'))
  browser=await p.chromium.launch(**({'executable_path':str(binaries[-1])} if binaries else {}))
  try:
   for label,landing in [('future','https://www.dropbox.com/t/8tb3nOWN0x7l6Hlq'),('historical','https://www.dropbox.com/t/yWLAXn40ZjqwjDlD')]:
    page=await browser.new_page();listed=asyncio.Event();download_ready=asyncio.Event()
    async def capture(response,label=label,listed=listed,download_ready=download_ready):
     if '/files/list_logged_out' in response.url:
      (session/(label+'-list.json')).write_text(await response.text())
      (session/(label+'-request.json')).write_text(json.dumps({'url':response.url,'headers':await response.request.all_headers(),'post_data':response.request.post_data}))
      listed.set()
     if '/files/download_logged_out' in response.url:
      (session/'download-request.json').write_text(json.dumps({'url':response.url,'headers':await response.request.all_headers(),'post_data':response.request.post_data}))
      download_ready.set()
    async def cancel_download(download):await download.cancel()
    page.on('response',capture);page.on('download',cancel_download)
    await page.goto(landing,wait_until='domcontentloaded');await asyncio.wait_for(listed.wait(),60)
    await page.close()
  finally:await browser.close()
asyncio.run(bootstrap())

futureq=json.loads((session/'future-request.json').read_text());histq=json.loads((session/'historical-request.json').read_text())
futfiles=json.loads((session/'future-list.json').read_text())['files'];histfiles=json.loads((session/'historical-list.json').read_text())['files']
jobs=[]
for scenario,years,files,q,landing in [('Historical',range(1995,2015),histfiles,histq,'https://www.dropbox.com/t/yWLAXn40ZjqwjDlD'),('ssp245',range(2041,2061),futfiles,futureq,'https://www.dropbox.com/t/8tb3nOWN0x7l6Hlq')]:
 for year in years:
  f=next(x for x in files if x['relative_path']==f'ET_daily_{year}_FWI_MRI-ESM2-0_{scenario}.tif');jobs.append((f,q,landing,year,scenario))
# Store a public inventory without transient signed links or session headers.
inv=[dict(filename=f['relative_path'],source_size_bytes=f['file_size'],year=y,scenario=s,landing_url=u) for f,q,u,y,s in jobs]
(out/'annual-file-inventory.json').write_text(json.dumps(inv,indent=2)+'\n')
def work(job):
 f,q,landing,year,scenario=job;name=f['relative_path'];p=out/('galicia-bbox-'+name)
 for attempt in range(3):
  try:
   if not p.exists():
    headers={k:v for k,v in q['headers'].items() if not k.startswith(':') and k not in ['content-length','accept-encoding']};headers['accept-encoding']='identity'
    payload=dict(transfer_id=json.loads(q['post_data'])['transfer_id'],requested_files_by_id=[f['transfer_file_id']],is_preview_download=True)
    req=urllib.request.Request('https://www.dropbox.com/2/file_transfers/files/download_logged_out',data=json.dumps(payload).encode(),headers=headers)
    with urllib.request.urlopen(req,timeout=30) as res:u=json.load(res)['url']
    with rasterio.Env(GDAL_DISABLE_READDIR_ON_OPEN='EMPTY_DIR',GDAL_HTTP_TIMEOUT='45'):
     with rasterio.open(u) as ds:
      assert ds.count==365+int(calendar.isleap(year)),(name,ds.count)
      w=from_bounds(-9.35,41.75,-6.7,43.85,ds.transform).round_offsets().round_lengths();a=ds.read(window=w);pr=ds.profile;pr.update(width=a.shape[2],height=a.shape[1],transform=ds.window_transform(w),compress='lzw')
      temp=p.with_suffix('.tmp.tif')
      with rasterio.open(temp,'w',**pr) as dst:dst.write(a)
      temp.replace(p)
   with rasterio.open(p) as ds:
    assert ds.count==365+int(calendar.isleap(year))
    meta=dict(filename=name,year=year,scenario=scenario,bands=ds.count,shape=list(ds.shape),transform=list(ds.transform),source_crs=str(ds.crs),nodata='NaN',valid_spatial_pixels=int(np.isfinite(ds.read(1)).sum()))
   b=p.read_bytes();rec=dict(path=str(p.relative_to(root)),url=landing,provider_filename=name,sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),acquired_at=datetime.datetime.fromtimestamp(p.stat().st_mtime,datetime.timezone.utc).isoformat(),processing='Native-grid HTTP range crop, all daily bands; 365 or366 followingactualsourcecount, no CRS assigned, no resampling. Baseline1995–2014/future2041–2060; MRI-ESM2-0 only.')
   print('OK',year,scenario,len(b),flush=True);return dict(artifact=rec,metadata=meta)
  except Exception as e:
   if attempt==2:return dict(error=str(e).split('?')[0][:300],filename=name)
   time.sleep(2)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 results=list(pool.map(work,jobs))
(out/'annual-crop-metadata.json').write_text(json.dumps(results,indent=2)+'\n')
records=[x['artifact'] for x in results if 'artifact' in x]
for p in [out/'annual-file-inventory.json',out/'annual-crop-metadata.json']:
 b=p.read_bytes();records.append(dict(path=str(p.relative_to(root)),url=None,sha256=hashlib.sha256(b).hexdigest(),size_bytes=len(b),acquired_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),processing='Locally generated acquisition inventory or crop metadata.'))
(root/'research/galicia-fire9km-annual-artifacts.json').write_text(json.dumps({'artifacts':records},indent=2)+'\n')
print('COMPLETED',len(records)-2,'of40',flush=True)

# Remove transient browser session headers after acquisition.
import shutil
shutil.rmtree(session, ignore_errors=True)
