"""Check source references, sizes and hashes for locally acquired files."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
sources = json.loads((ROOT / 'research/sources.json').read_text())
ids = [s['id'] for s in sources]
assert len(ids) == len(set(ids)), 'Duplicate source IDs'
manifest = json.loads((ROOT / 'data/manifest.json').read_text())
for entry in manifest:
    assert entry['source_id'] in ids, entry['source_id']
    path = (ROOT / entry['path']).resolve()
    assert path.is_relative_to(ROOT / 'data'), entry['path']
    assert path.is_file(), f'Missing local file: {path}'
    body = path.read_bytes()
    assert len(body) == entry['bytes'], f'Size mismatch: {path}'
    assert hashlib.sha256(body).hexdigest() == entry['sha256'], f'Hash mismatch: {path}'
print(f'Verified {len(manifest)} local artifacts and {len(sources)} source records')
