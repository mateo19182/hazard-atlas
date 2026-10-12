"""Render the atlas from computed data, without repeating the scientific pipeline."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/derived/galicia'

def render():
    data_path = OUT / 'report-data.json'
    payload = json.loads(data_path.read_text())
    files = {key: ROOT / 'web' / filename for key, filename in [
        ('html', 'index.template.html'), ('css', 'atlas.css'), ('js', 'atlas.js')]}
    page = files['html'].read_text().replace('__STYLE__', files['css'].read_text())
    page = page.replace('__SCRIPT__', files['js'].read_text())
    page = page.replace('__DATA__', json.dumps(payload, ensure_ascii=False, allow_nan=False).replace('</', '<\\/'))
    target = OUT / 'galicia.html'
    target.write_text(page)
    record = {'data_sha256': hashlib.sha256(data_path.read_bytes()).hexdigest(),
              'sources': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files.values()},
              'output_sha256': hashlib.sha256(target.read_bytes()).hexdigest()}
    (OUT / 'page-provenance.json').write_text(json.dumps(record, indent=2) + '\n')
    print(target)

if __name__ == '__main__':
    render()
