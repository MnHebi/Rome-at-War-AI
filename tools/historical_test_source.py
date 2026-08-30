"""Immutable diagnostic-stage fixtures, distinct from current behavioral source."""
import io
from pathlib import Path
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]
DIAGNOSTIC_BASE = 'a5de7d85bad71f36f4c8903747908d71ac164a7e'


def historical_source(name):
    return subprocess.check_output(['git', 'show', f'{DIAGNOSTIC_BASE}:{name}'],
                                   cwd=ROOT).decode('utf-8-sig')


def historical_runtime():
    archive = subprocess.check_output(['git', 'archive', DIAGNOSTIC_BASE], cwd=ROOT)
    with tarfile.open(fileobj=io.BytesIO(archive)) as data:
        return {p.name: data.extractfile(p).read() for p in data.getmembers()
                if '/' not in p.name and p.name.endswith(('.per', '.ai'))}
