"""Seal or check the October 18 public release; exclude the later private audit."""
import argparse
from hashlib import sha256
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'overall_llm_expanded_2026-10-18/release_checksums.json'
SOURCES = ['README.md', 'FUNCTIONS.md', 'OUTPUT_COMPLIANCE.md', 'LLM_EXPANSION.md',
           'docs/index.html', 'docs/functions.html', 'docs/output_compliance.html',
           '.github/workflows/validate.yml', '.github/workflows/october18-validate.yml', 'requirements-reports.txt',
           'llm_field_2026_10_18.py', 'test_llm_field_2026_10_18.py',
           'llm_screening_2026_10_18.py', 'test_llm_screening_2026_10_18.py',
           'tev_native_adapter_2026_10_18.py', 'test_tev_native_adapter_2026_10_18.py',
           'tev_screening_2026_10_18.py', 'llm_expansion_analysis_2026_10_18.py',
           'test_llm_expansion_analysis_2026_10_18.py', 'plot_llm_expansion.py',
           'build_llm_expansion_report.py', 'build_october18_report.py',
           'test_october18_publication.py', 'freeze_october18_release.py',
           'archive_october16_publication.py', 'test_publication.py', 'test_overall.py']
FOLDERS = ['native_additions_2026-10-18', 'overall_expanded_2026-10-18',
           'llm_additions_2026-10-18', 'overall_llm_expanded_2026-10-18',
           'docs/figures/october18', 'publication_archive_2026-10-16']


def hashes():
    paths = {ROOT / name for name in SOURCES}
    paths.update(path for folder in FOLDERS for path in (ROOT / folder).rglob('*') if path.is_file())
    paths.discard(DEST)
    assert all(path.exists() for path in paths)
    assert all('runs' not in p.relative_to(ROOT).parts and 'hardening_2026-10-18' not in p.relative_to(ROOT).parts for p in paths)
    return {str(path.relative_to(ROOT)): sha256(path.read_bytes()).hexdigest() for path in sorted(paths)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    value = hashes()
    if args.check:
        assert json.loads(DEST.read_text()) == value, 'October18 release content differs from its seal'
        print('PASS:', len(value), 'public release files; later hardening project and private audit excluded')
    else:
        DEST.write_text(json.dumps(value, indent=2) + '\n')
        print('Sealed', len(value), 'public release files; earlier release seals unchanged')
