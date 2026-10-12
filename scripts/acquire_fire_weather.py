"""Acquire published FIRE-RES summer FWI means using bounded ZIP HTTP ranges.

No shared catalog or manifest mutation. Writes a standalone provenance fragment.
"""
import urllib.request,io,zipfile,json,hashlib
from datetime import datetime, timezone
from pathlib import Path
class Remote(io.RawIOBase):
 def __init__(self,u,size):self.u=u;self.size=size;self.pos=0
 def seekable(self):return True
 def readable(self):return True
 def seek(self,o,w=0):self.pos=o if w==0 else self.pos+o if w==1 else self.size+o;return self.pos
 def tell(self):return self.pos
 def read(self,n=-1):
  if n<0:n=self.size-self.pos
  if n==0:return b''
  if n>2_000_000:raise RuntimeError('Range exceeds 2 MB acquisition bound')
  req=urllib.request.Request(self.u,headers={'Range':f'bytes={self.pos}-{self.pos+n-1}'})
  with urllib.request.urlopen(req,timeout=40) as r:
   if r.status!=206:raise RuntimeError('No range support')
   d=r.read()
  if len(d)!=n:raise RuntimeError((len(d),n))
  self.pos+=len(d);return d
u='https://zenodo.org/records/11083641/files/EU_DATA.zip?download=1'
z=zipfile.ZipFile(Remote(u,8509078988))
root=Path(__file__).resolve().parents[1]
o=root/'data/raw/public/galicia-fire-weather';o.mkdir(parents=True,exist_ok=True)
artifacts=[]
for n in z.namelist():
 if '/indices/JJA_FWI_' in n:
  p=o/Path(n).name
  if not p.exists():p.write_bytes(z.read(n))
  artifacts.append({'source_id':'fire-res-future-fwi','path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'url':u,'archive_member':n,'acquired_at':datetime.now(timezone.utc).isoformat(),'license':'CC-BY-4.0','method':'ZIP member extracted through validated HTTP206 byte ranges; ZIP CRC checked by zipfile'})
  print(n,p.stat().st_size,flush=True)
(o/'fire-res-provenance.json').write_text(json.dumps(artifacts,indent=2)+'\n')
