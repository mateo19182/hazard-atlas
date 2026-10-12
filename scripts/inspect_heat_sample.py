# /// script
# dependencies = ["xarray==2026.4.0", "h5netcdf", "h5py"]
# ///
"""Inspect the acquired AdapteCCa sample without computing place rankings."""
from pathlib import Path
import hashlib
import json
import xarray as xr

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'data/manifest.json').read_text())
entry = next(m for m in manifest if m['source_id'] == 'adaptecca-heat-ssp245')
path = root / entry['path']
assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256']
with xr.open_dataset(path) as ds:
    summary = {
        'source_id': entry['source_id'], 'input_sha256': entry['sha256'],
        'dimensions': dict(ds.sizes), 'attributes': dict(ds.attrs),
        'members': ds.member.values.tolist(), 'periods': ds.period.values.tolist(),
        'time_filters': ds.time_filter.values.tolist(),
        'variables': {k: dict(v.attrs) for k, v in ds.data_vars.items()},
        'coordinate_ranges': {k: [float(ds[k].min()), float(ds[k].max())]
                              for k in ['lat', 'lon']},
        'interpretation': '11 model members plus an average, not 12 independent models. Period year bounds require external documentation. Heatwave duration is relative to a local percentile, not absolute heat severity.'
    }
    probe = ds.tasmaxhwdmax.sel(member='average', period='medium_future', time_filter='year').load()
    summary['data_read_check'] = {'finite_cells': int(probe.count()),
                                 'minimum': float(probe.min()), 'maximum': float(probe.max()),
                                 'scope': 'Full supplied rectangular grid; not a Spain statistic or ranking.'}
out = root / 'data/derived/adaptecca-heat-sample-inspection.json'
out.write_text(json.dumps(summary, indent=2) + '\n')
print(out)
print(json.dumps(summary['data_read_check']))
