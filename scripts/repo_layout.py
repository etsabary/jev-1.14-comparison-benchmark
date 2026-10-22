"""Current source locations and exact pre-layout bytes for dated evidence.

Live runners must use ``source_file`` for dependencies in scripts/. Only checks
against already-published provenance use ``frozen_file``. No release manifest,
measurement, question, or dated report is rewritten by this path migration.
"""
from hashlib import sha256
from functools import lru_cache
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'scripts'
ARCHIVE = SCRIPTS / 'legacy_layout'
MANIFEST = SCRIPTS / 'layout_manifest.json'


@lru_cache(maxsize=4)
def _manifest(path, modified_ns):
    return json.loads(path.read_text())


def source_file(path):
    """Resolve a former root-level Python filename to its active source."""
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    if path.parent == ROOT and path.suffix == '.py':
        return SCRIPTS / path.name
    return path


def frozen_file(path):
    """Resolve only registered superseded files to checksum-checked snapshots."""
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    try:
        name = path.relative_to(ROOT).as_posix()
    except ValueError:
        return path
    manifest = _manifest(MANIFEST, MANIFEST.stat().st_mtime_ns)
    if name in manifest['moved_sources'].values():
        name = path.name
    entries = manifest['preserved_sources']
    entry = entries.get(name)
    if entry is None:
        return path
    saved = ROOT / entry['archive_path']
    assert saved.resolve().is_relative_to(ARCHIVE.resolve()), name
    assert sha256(saved.read_bytes()).hexdigest() == entry['sha256'], name
    return saved


def verify_software(saved, current, *, historical=False):
    """Offline audits may check archived code; live resume remains current-only."""
    if saved == current:
        return
    assert historical, 'Frozen execution software changed'
    assert set(saved) == set(current), 'Frozen execution dependency set changed'
    for name, expected in saved.items():
        path = frozen_file(ROOT / name)
        assert path.is_relative_to(ARCHIVE), 'No archived execution source: ' + name
        assert sha256(path.read_bytes()).hexdigest() == expected, name
