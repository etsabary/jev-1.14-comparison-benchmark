"""Create a public-safe correction bundle inside the private build, offline.

This never touches the GitHub checkout. Original fresh ledgers/plans are already
sanitized at capture; exact copies preserve dispatch and completion bindings.
Environment-variable names in a model specification are not credential values.
No private answer key, per-item correctness or owner path is exported.
"""
from copy import deepcopy
import argparse
import csv
import io
import json
from pathlib import Path

import assemble_corrected as assembly
from validate_corrected_public import privacy_guard,file_hash,validate

ROOT=Path(__file__).resolve().parent


def dump(value):return (json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()


def export(benchmark_root,build=assembly.OUT,retests=assembly.RETESTS,destination=None):
    root,build,retests=Path(benchmark_root),Path(build),Path(retests)
    destination=Path(destination) if destination else build/'ready_to_publish'
    assert not destination.exists(),'Public bundle already exists; do not silently overwrite'
    checks=json.loads((build/'checksums.json').read_text())
    for name,expected in checks.items():assert file_hash(build/name)==expected,'Changed private assembled artifact'
    summary=deepcopy(json.loads((build/'summary.json').read_text()))
    original_plan=json.loads((retests/'frozen_plan.json').read_text())
    private_sources=summary.pop('private_retest_sources_sha256')
    summary['replacement_retest_plan_sha256']=summary.pop('private_retest_plan_sha256')
    assert file_hash(retests/'frozen_plan.json')==summary['replacement_retest_plan_sha256']
    payload={name:(build/name).read_bytes() for name in ('questions_1136.csv','item_metadata.csv','selection_manifest.json')}
    payload['replacement_evidence/frozen_plan.json']=(retests/'frozen_plan.json').read_bytes()
    payload['replacement_evidence/candidate_rows.json']=(retests/'candidate_rows.json').read_bytes()
    payload['replacement_evidence/route_overrides.json']=dump(original_plan['route_overrides'])
    for relative,expected in private_sources.items():
        assert file_hash(retests/relative)==expected
        payload['replacement_evidence/'+relative]=(retests/relative).read_bytes()
    # Completion files bind the dispatch ledger; export it and all other bound
    # files exactly, not rewritten under a misleading original checksum.
    for mid in summary['models']:
        folder=retests/'models'/mid.replace('/','__')
        for name in ('dispatches.jsonl','attempts.jsonl','results.jsonl','retry_waits.jsonl','metadata_checkpoint.json','COMPLETED.json'):
            payload['replacement_evidence/models/'+mid.replace('/','__')+'/'+name]=(folder/name).read_bytes()
    blocked=retests/'models/nimble_v4'
    for name in ('metadata_checkpoint.json','UNAVAILABLE.json'):
        if (blocked/name).exists():payload['replacement_evidence/models/nimble_v4/'+name]=(blocked/name).read_bytes()
    summary['replacement_evidence_sha256']={name:assembly.digest(retests/name) for name in private_sources}
    source_models={};source_digests={}
    original_summary=json.loads((root/assembly.retest.SUMMARY).read_text())
    for mid in summary['models']:
        spec=original_plan['models'][mid]
        _,source=assembly.original_source(root,mid,spec,original_summary)
        source_models[mid]={'original_attempts':source,'model_requested':spec['model'],
            'original_unchanged_cases':1134,'replacement_cases':2,
            'source_url':'https://github.com/etsabary/jev-1.14-comparison-benchmark/blob/main/'+source}
        source_digests[source]=file_hash(root/source)
    source={'status':'PUBLIC_SAFE_CORRECTED_EVIDENCE_INDEX','original_sources_sha256':source_digests,
        'models':source_models,'retired_item_ids':summary['retired_parent_ids'],
        'replacement_item_ids':summary['replacement_ids'],
        'original_summary_sha256':summary['original_evidence_validation']['original_summary_sha256'],
        'private_key_policy':'No key or individual correctness exported; original40 primary/eventual scores were reproduced offline with the external frozen key',
        'accuracy_limit':'Public validator checks evidence/timing/cost/coverage and aggregate consistency; exact correctness requires the private key',
        'unavailable_original_model':'Nimble v4 has1134 unchanged cases only and is excluded from active full-bank ranking',
        'route_changes':{mid:summary['models'][mid]['replacement_provenance'] for mid in summary['models'] if summary['models'][mid]['replacement_provenance']['route_changed_for_replacements']}}
    payload['source_manifest.json']=dump(source)
    payload['summary.json']=dump(summary)
    buf=io.StringIO(newline='');writer=csv.writer(buf)
    order=list(summary['models'])
    writer.writerow(['family_id','family','n',*[summary['models'][m]['label'] for m in order]])
    for family in summary['by_family']:writer.writerow([family['family_id'],family['family'],family['n'],*[family['models'][m]['correct'] for m in order]])
    payload['family_comparison.csv']=buf.getvalue().encode()
    for name in ('validate_corrected_public.py','export_corrected.py','assemble_corrected.py',
                 'test_assemble_corrected.py','test_export_corrected.py'):
        payload['source/'+name]=(ROOT/name).read_bytes()
    for name,data in payload.items():privacy_guard(data)
    destination.mkdir(parents=True)
    for relative,data in payload.items():
        path=destination/relative;path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data)
    checksum={relative:file_hash(destination/relative) for relative in sorted(payload)}
    (destination/'checksums.json').write_bytes(dump(checksum))
    result=validate(destination,root)
    return destination,result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark-root',type=Path,required=True)
    parser.add_argument('--build',type=Path,default=assembly.OUT)
    parser.add_argument('--retests',type=Path,default=assembly.RETESTS)
    parser.add_argument('--destination',type=Path)
    args=parser.parse_args();path,result=export(args.benchmark_root,args.build,args.retests,args.destination)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
