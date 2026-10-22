"""Resolve the exact October 19 presentation for its unchanged release checks."""
from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
ARCHIVE=ROOT/'direct_archive_2026-10-20'


def previous_path(path):
    path=Path(path)
    manifest=ARCHIVE/'manifest.json'
    entries=json.loads(manifest.read_text())['files'] if manifest.exists() else {}
    entry=entries.get(str(path.relative_to(ROOT)))
    if entry is None:return path
    saved=ARCHIVE/entry['path']
    assert saved.resolve().is_relative_to(ARCHIVE.resolve())
    assert sha256(saved.read_bytes()).hexdigest()==entry['sha256'],path
    return saved

