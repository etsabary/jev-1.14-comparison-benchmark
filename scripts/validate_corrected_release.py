"""Validate current corrected evidence, presentation and independent source seals."""
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FOLDER = ROOT / 'corrected_2026-10-18'


def validator():
    spec = importlib.util.spec_from_file_location('corrected_public_validator', FOLDER / 'source/validate_corrected_public.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate():
    module = validator()
    result = module.validate(FOLDER, ROOT)
    s = json.loads((FOLDER / 'summary.json').read_text())
    assert s['original_evidence_validation']['complete_original_primary_and_eventual_scores_reproduced'] == 40
    assert sum(v['by_role']['core']['attempted'] for v in s['models'].values()) == 36*640
    for p in FOLDER.rglob('*'):
        if p.is_file() and p.suffix in ('.json', '.jsonl', '.csv', '.md', '.py'):
            module.privacy_guard(p.read_bytes())
    receipt = json.loads((FOLDER / 'correction_receipt.json').read_text())
    assert receipt['fresh_primary_cases'] == 72 and receipt['fresh_recoveries'] == 0
    assert receipt['corrected_question_bank_sha256'] == sha256((FOLDER / 'questions_1136.csv').read_bytes()).hexdigest()
    if (FOLDER / 'release_checksums.json').exists():
        from freeze_corrected_release import hashes
        assert hashes() == json.loads((FOLDER / 'release_checksums.json').read_text()), 'Current corrected-release seal differs'
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    validate()
