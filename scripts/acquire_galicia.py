"""Acquire bounded inputs for the Galicia pilot; record immutable file hashes."""
from pathlib import Path
from urllib.request import urlopen
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://escenarios.adaptecca.es/thredds/fileServer/peninsula/Proyecciones_CMIP6_en_rejilla/Climatologia/'
ITEMS = [
 ('adaptecca-heat-ssp245', 'CMIP6 heatwave duration SSP245 sample', BASE+'Temperatura/tasmaxhwdmax/climatology_CMIP6_ESD-RegBA_tasmaxhwdmax_ssp245.nc', '.nc'),
 ('galicia-boundary', 'Galicia GISCO NUTS 2024 boundary', 'https://gisco-services.ec.europa.eu/distribution/v2/nuts/distribution/ES11-region-01m-4326-2024.geojson', '.geojson'),
 ('adaptecca-definitions-2025', 'AdapteCCa data description v7 June 2025', 'https://escenarios.adaptecca.es/doc/datos.pdf?v=202506', '.pdf'),
]
for category, method, variable in [('Temperatura','ESD-RegBA','tasmaxmax'), ('Precipitacion','deepESD','prspellb1'), ('Precipitacion','deepESD','prmax24')]:
 for scenario in ['ssp245','ssp370']:
  ITEMS.append((f'adaptecca-{variable}-{scenario}',f'AdapteCCa {variable} {scenario}',BASE+f'{category}/{variable}/climatology_CMIP6_{method}_{variable}_{scenario}.nc','.nc'))

def acquire(item):
 sid, title, url, suffix = item
 with urlopen(url, timeout=60) as response:
  body = response.read(200_000_001)
  resolved, content_type = response.url, response.headers.get('Content-Type', '')
 if not body or len(body)>200_000_000:
  raise ValueError(f'Invalid size for {sid}')
 digest=hashlib.sha256(body).hexdigest()
 path=ROOT/'data/raw/public'/f'{sid}-{digest[:12]}{suffix}'
 path.write_bytes(body)
 return dict(id=sid,title=title,url=url,kind='dataset' if suffix in ['.nc','.geojson'] else 'documentation',review_status='acquired for Galicia pilot',acquisition_status='local_artifact_preserved',rights_status='see original source and embedded metadata'), dict(source_id=sid,path=str(path.relative_to(ROOT)),sha256=digest,bytes=len(body),acquired_at=datetime.now(timezone.utc).isoformat(),requested_url=url,resolved_url=resolved,content_type=content_type,method='HTTP download',redistribution='see original source terms')

def main():
 sp=ROOT/'research/sources.json';mp=ROOT/'data/manifest.json'
 sources=json.loads(sp.read_text());manifest=json.loads(mp.read_text())
 existing={a['source_id'] for a in manifest if (ROOT/a['path']).exists()}
 with ThreadPoolExecutor(max_workers=2) as pool:
  for source,entry in pool.map(acquire,[i for i in ITEMS if i[0] not in existing]):
   if not any(s['id']==source['id'] for s in sources):sources.append(source)
   manifest.append(entry)
   sp.write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
   mp.write_text(json.dumps(manifest,indent=2)+'\n')
   print(source['id'],entry['bytes'],flush=True)

if __name__=='__main__': main()
