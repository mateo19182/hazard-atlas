"""Preserve selected small reference snapshots. Does not acquire hazard rasters."""
from pathlib import Path
from urllib.request import Request, urlopen
import datetime
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SELECTED = {'thinkhazard', 'thinkhazard-classification', 'thinkhazard-data',
            'unicef-mhi-readme', 'unicef-mhi-code', 'unicef-mhi-inputs',
            'antofie-2025', 'espon-titan', 'inform', 'ericc'}

def main():
    sources = json.loads((ROOT / 'research/sources.json').read_text())
    manifest_path = ROOT / 'data/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    for source in sources:
        if source['id'] not in SELECTED:
            continue
        if any(m['source_id'] == source['id'] and (ROOT / m['path']).exists()
               for m in manifest):
            continue
        try:
            req = Request(source['url'], headers={'User-Agent': 'HazardAtlasResearch/0.1'})
            with urlopen(req, timeout=20) as response:
                body = response.read(10_000_001)
                content_type = response.headers.get('Content-Type', '')
                final_url = response.url
            if not body or len(body) > 10_000_000:
                raise ValueError('Empty response or exceeds 10 MB snapshot limit')
            suffix = '.ipynb' if source['url'].endswith('.ipynb') else '.js' if source['url'].endswith('.js') else '.md' if source['url'].endswith('.md') else '.html'
            digest = hashlib.sha256(body).hexdigest()
            dest = ROOT / 'data/raw/public' / (source['id'] + '-' + digest[:12] + suffix)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(body)
            manifest.append(dict(source_id=source['id'], path=str(dest.relative_to(ROOT)),
                                 sha256=digest, bytes=len(body),
                                 acquired_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                                 method='HTTP snapshot', requested_url=source['url'],
                                 resolved_url=final_url, content_type=content_type,
                                 redistribution='not cleared', content_validation='retrieved; semantic completeness not verified'))
            source['acquisition_status'] = 'snapshot_downloaded'
            source.pop('acquisition_error', None)
            print('Saved', source['id'], len(body), 'bytes')
        except Exception as exc:
            source['acquisition_status'] = 'download_failed'
            source['acquisition_error'] = str(exc)
            print('Failed', source['id'], str(exc))
        manifest_path.write_text(json.dumps(manifest, indent=2) + '\n')
        (ROOT / 'research/sources.json').write_text(json.dumps(sources, indent=2, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
