"""Key-free corrected-release evidence validator. No network or inference.

Reconstruct selected1134+2 first-attempt records from checksum-linked original
ledgers and the replacement ledgers. Verify timing/cost/coverage and aggregate
consistency. Accuracy itself requires the private frozen key; this validator
does not infer or publish that key or individual correctness.
"""
from collections import Counter,defaultdict
from decimal import Decimal
from hashlib import sha256
import argparse
import csv
import json
from pathlib import Path
import re


def file_hash(path):return sha256(Path(path).read_bytes()).hexdigest()


def privacy_guard(data):
    text=data.decode('utf-8')
    private_roots='/'+'Users/'+'|'+'/'+'home/'
    assert not re.search(private_roots+r'|sk-(?:or-v1-)?[A-Za-z0-9_-]{24,}',text),'Private path/credential-like string'
    try:
        parsed=json.loads(text)
    except ValueError:
        try:parsed=[json.loads(line) for line in text.splitlines() if line.strip()]
        except ValueError:return
    forbidden={'user_id','account_id','authorization','api_key','access_token','refresh_token','credits','cost_details',
               'gold_option','gold_text','gold_canonical','gold_answer','correct_first','correct_eventual',
               'choice_first_correct','choice_eventual_correct'}
    def inspect(value):
        if isinstance(value,dict):
            assert not {str(k).lower() for k in value}&forbidden,'Private/correctness field'
            if 'key_name' in value:assert value['key_name'] in ('OPENROUTER_API_KEY','BESPOKE_API_KEY')
            for child in value.values():inspect(child)
        elif isinstance(value,list):
            for child in value:inspect(child)
    inspect(parsed)


def records(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def firsts(attempts):
    groups=defaultdict(list)
    for row in attempts:groups[row['item_id']].append(row)
    result={}
    for item,group in groups.items():
        group=sorted(group,key=lambda r:int(r['attempt']))
        assert [int(r['attempt']) for r in group] in ([1],[1,2])
        result[item]=group[0]
    return result


def money(attempts,reported_only=False):
    values=[]
    for r in attempts:
        value=r.get('reported_cost_usd')
        if not reported_only and r.get('accounted_cost_usd') is not None:value=r['accounted_cost_usd']
        if value is not None:values.append(Decimal(str(value)))
    total=sum(values,Decimal(0))
    return {'known_usd':float(total),'exact_usd':str(total),'reported_attempts':len(values),'missing_attempts':len(attempts)-len(values)}


def quantiles(values):
    values=sorted(values)
    def q(p):
        x=(len(values)-1)*p;lo=int(x)
        return values[lo]+(values[min(lo+1,len(values)-1)]-values[lo])*(x-lo)
    return {'n':len(values),'median_ms':q(.5) if values else None,'p95_ms':q(.95) if values else None}


def checked_source(root,relative,expected,source_map):
    path=Path(root)/source_map.get(relative,relative)
    assert path.resolve().is_relative_to(Path(root).resolve()),'Source mapping escapes benchmark root'
    assert file_hash(path)==expected,'Original evidence checksum differs: '+relative
    return path


def validate(export_dir,benchmark_root,source_map=None):
    out=Path(export_dir);root=Path(benchmark_root);source_map=source_map or {}
    checks=json.loads((out/'checksums.json').read_text())
    for relative,expected in checks.items():
        path=out/relative;assert path.resolve().is_relative_to(out.resolve())
        assert file_hash(path)==expected,'Changed public export: '+relative
        privacy_guard(path.read_bytes())
    summary=json.loads((out/'summary.json').read_text())
    source=json.loads((out/'source_manifest.json').read_text())
    plan=json.loads((out/'replacement_evidence/frozen_plan.json').read_text())
    assert file_hash(out/'replacement_evidence/frozen_plan.json')==summary['replacement_retest_plan_sha256']
    assert len(summary['models'])==summary['model_count']==36
    assert set(summary['models'])==set(summary['publication']['eligible_model_ids'])
    assert 'nimble_v4' not in summary['models']
    with (out/'questions_1136.csv').open(newline='') as stream:bank=list(csv.DictReader(stream))
    with (out/'item_metadata.csv').open(newline='') as stream:metadata={r['item_id']:r for r in csv.DictReader(stream)}
    ids={r['item_id'] for r in bank};assert len(bank)==len(ids)==1136
    assert ids==set(metadata) and sum(r['role']=='core' for r in metadata.values())==640
    assert not ids&set(source['retired_item_ids'])
    assert set(source['replacement_item_ids'])<=ids
    cache={};selected_all=[];primary={}
    for mid,value in summary['models'].items():
        spec=source['models'][mid];relative=spec['original_attempts']
        if relative not in cache:
            path=checked_source(root,relative,source['original_sources_sha256'][relative],source_map)
            cache[relative]=records(path)
        original=[r for r in cache[relative] if r.get('model_requested')==spec['model_requested']]
        assert len(firsts(original))==1136
        retained=[r for r in original if r['item_id'] not in source['retired_item_ids']]
        newpath=out/'replacement_evidence/models'/mid.replace('/','__')
        completion=json.loads((newpath/'COMPLETED.json').read_text());assert completion['status']=='COMPLETE_TWO_CASES'
        for name,expected in completion['files_sha256'].items():assert file_hash(newpath/name)==expected
        replacement=records(newpath/'attempts.jsonl')
        assert set(firsts(replacement))==set(source['replacement_item_ids'])
        for row in replacement:
            assert not row.get('identity_issue')
            assert row.get('model_returned') in plan['models'][mid]['captured_returned_identities']
            assert row['prompt_sha256']==next(q['prompt_sha256'] for q in bank if q['item_id']==row['item_id'])
        selected=retained+replacement;first=firsts(selected);assert set(first)==ids
        ff=list(first.values());primary[mid]=first;selected_all.extend(selected)
        assert value['primary']['attempted']==len(ff)==1136
        assert value['primary']['answered']==sum(r['status']=='ok' for r in ff)
        assert value['cost_all_attempts']==money(selected)
        assert value['reported_api_cost_all_attempts']==money(selected,True)
        assert value['cost_first_attempts']==money(ff)
        assert value['latency_first_all']==quantiles([float(r['latency_ms']) for r in ff])
        assert value['latency_first_usable']==quantiles([float(r['latency_ms']) for r in ff if r['status']=='ok'])
        assert value['statuses_first']==dict(Counter(r['status'] for r in ff))
        assert value['by_role']['core']['attempted']==640
        assert sum(f['models'][mid]['correct'] for f in summary['by_family'])==value['primary']['correct']
        assert sum(v['correct'] for v in value['by_role'].values())==value['primary']['correct']
        assert sum(v['correct'] for v in value['by_level'].values())==value['primary']['correct']
        assert sum(value['dates_toronto'].values())==1136
    assert summary['total_selected_accounted_cost']==money(selected_all)
    assert summary['total_selected_reported_cost']==money(selected_all,True)
    assert summary['total_selected_http_attempts']==len(selected_all)
    for pair in summary['pairwise']:
        aa,bb=primary[pair['a']],primary[pair['b']]
        shared=[i for i in ids if aa[i]['status']=='ok' and bb[i]['status']=='ok']
        assert pair['both_answered']==len(shared)
        assert pair['same_choice_on_both_answered']==sum(aa[i]['choice']==bb[i]['choice'] for i in shared)
        assert pair['both_correct']+pair['both_unsuccessful']+pair['only_a_correct']+pair['only_b_correct']==1136
    return {'status':'PASS_KEY_FREE_EVIDENCE_CHECKS','models':36,'questions_each':1136,
            'replacement_primary_cases':72,'original_primary_cases_reused':36*1134,
            'accuracy_requires_private_key':True,'gold_or_individual_correctness_exported':False}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--export-dir',type=Path,required=True)
    parser.add_argument('--benchmark-root',type=Path,required=True)
    parser.add_argument('--source-map',type=Path,help='Optional relative-path map if original ledgers were archived')
    args=parser.parse_args();mapping=json.loads(args.source_map.read_text()) if args.source_map else None
    print(json.dumps(validate(args.export_dir,args.benchmark_root,mapping),indent=2))


if __name__=='__main__':main()
