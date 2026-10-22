"""Check the source-only layout migration without network calls or private data."""
import ast
from hashlib import sha256
import json
from pathlib import Path

from repo_layout import ARCHIVE, MANIFEST, ROOT, SCRIPTS, frozen_file, source_file


def validate():
    manifest = json.loads(MANIFEST.read_text())
    assert manifest['version'] == 'scripts-layout-2026-10-22-v1'
    assert len(manifest['moved_sources']) == 110
    assert not list(ROOT.glob('*.py')), 'Python sources remain in the repository root'
    for old, new in manifest['moved_sources'].items():
        assert '/' not in old and old.endswith('.py')
        assert new == 'scripts/' + old and not (ROOT / old).exists()
        assert source_file(ROOT / old) == ROOT / new
        assert (ROOT / new).is_file()
        preserved = frozen_file(ROOT / old)
        assert preserved.is_relative_to(ARCHIVE)
    for old, entry in manifest['preserved_sources'].items():
        assert frozen_file(ROOT / old) == ROOT / entry['archive_path']
    for name, expected in manifest['protected_files'].items():
        path = ROOT / name
        assert path.resolve().is_relative_to(ROOT.resolve()), name
        assert sha256(path.read_bytes()).hexdigest() == expected, 'Published evidence changed: ' + name
    assert manifest['current_files'], 'Active sources have not been bound'
    for name, expected in manifest['current_files'].items():
        assert sha256((ROOT / name).read_bytes()).hexdigest() == expected, 'Active source changed: ' + name
    actual = {p.relative_to(ROOT).as_posix() for p in SCRIPTS.glob('*.py')}
    assert actual <= manifest['current_files'].keys(), 'Unbound active Python source'
    for path in SCRIPTS.glob('*.py'):
        ast.parse(path.read_text(), filename=str(path))
    for name in ('README.md', '.github/workflows/validate.yml', '.github/workflows/october18-validate.yml'):
        assert name in manifest['current_files']
    readme = (ROOT / 'README.md').read_text()
    assert '[scripts/](scripts/README.md)' in readme
    assert 'python3 scripts/validate_october21_release.py' in readme
    print(f"PASS: 110 root sources relocated; {len(manifest['protected_files'])} published files unchanged; "
          f"{len(manifest['current_files'])} active files and all historical snapshots checked.")
    return manifest


if __name__ == '__main__':
    validate()
