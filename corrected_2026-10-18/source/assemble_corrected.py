"""Offline corrected-bank assembly; no inference or credential access.

An external original frozen key is used only in memory. Forty original primary
scores are reproduced before two retired prompts are removed. The36 continuous
routes receive exactly two fresh replacement responses; original Nimble v4 has
only1134 retained cases and is not ranked. No original artifact is modified.
"""
from collections import Counter, defaultdict
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
import argparse
import csv
from datetime import datetime
import io
import itertools
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import retest_replacements as retest

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'runs/corrected_release_build_2026-10-18'
REPAIRS=ROOT/'runs/repair_design_2026-10-18'
RETESTS=retest.RUNS


def digest(path):return sha256(Path(path).read_bytes()).hexdigest()


def replace_ids(value,mapping):
    if isinstance(value,str):return mapping.get(value,value)
    if isinstance(value,list):return [replace_ids(v,mapping) for v in value]
    if isinstance(value,dict):return {mapping.get(k,k):replace_ids(v,mapping) for k,v in value.items()}
    return value


def corrected_bank(old_rows,metadata,selection,candidates,repairs,keys):
    """Construct corrected inputs and private key in memory; no key serialization."""
    mapping={r['parent_item_id']:r['new_item_id'] for r in repairs}
    assert len(mapping)==2 and len(set(mapping.values()))==2
    old={r['item_id']:r for r in old_rows};new={r['item_id']:r for r in candidates}
    assert set(mapping)<=set(old) and set(new)==set(mapping.values()) and not set(new)&set(old)
    assert set(old)<=set(keys)
    corrected_keys={i:deepcopy(k) for i,k in keys.items() if i in old and i not in mapping}
    for parent,replacement in mapping.items():
        row=new[replacement];original=old[parent]
        assert all(row[k]==original[k] for k in original if k not in ('item_id','question','prompt_text','prompt_sha256'))
        assert row['prompt_text']==original['prompt_text'].replace(original['question'],row['question'])
        corrected_keys[replacement]={**deepcopy(keys[parent]),'item_id':replacement}
    bank=[deepcopy(new[mapping[r['item_id']]]) if r['item_id'] in mapping else deepcopy(r) for r in old_rows]
    md=replace_ids(metadata,mapping)
    for row in md:
        if row['item_id'] in new:row['prompt_sha256']=new[row['item_id']]['prompt_sha256']
    assert {r['item_id'] for r in bank}=={r['item_id'] for r in md}==set(corrected_keys)
    assert len(bank)==len(old_rows) and Counter(r['role'] for r in md)==Counter(r['role'] for r in metadata)
    return bank,md,replace_ids(selection,mapping),corrected_keys,mapping


def first_eventual(attempts):
    groups=defaultdict(list)
    for row in attempts:groups[row['item_id']].append(row)
    first,eventual={},{}
    for item,group in groups.items():
        group=sorted(group,key=lambda a:int(a['attempt']))
        assert [int(a['attempt']) for a in group] in ([1],[1,2]),'Duplicate or incomplete attempt sequence'
        first[item],eventual[item]=group[0],group[-1]
    return first,eventual


def normalize(row,native):
    return {**row,'normalized_status':row['status'],'normalized_choice':row.get('choice') or '',
            'normalized_confidence':row.get('confidence') if native and row['status']=='ok' else None,
            'probability_warning':'Missing or non-normalized probabilities' if native and row['status']=='ok' and not row.get('probabilities_valid') else ''}


def monetary(attempts,reported_only=False):
    values=[]
    for row in attempts:
        value=row.get('reported_cost_usd')
        if not reported_only and row.get('accounted_cost_usd') is not None:value=row['accounted_cost_usd']
        if value is not None:values.append(Decimal(str(value)))
    total=sum(values,Decimal(0))
    return {'known_usd':float(total),'exact_usd':str(total),'reported_attempts':len(values),
            'missing_attempts':len(attempts)-len(values)}


def select_replacements(original,replacements,parent_ids,new_ids):
    assert len(set(parent_ids))==len(set(new_ids))==2
    retired=[r for r in original if r['item_id'] in parent_ids]
    kept=[r for r in original if r['item_id'] not in parent_ids]
    first,last=first_eventual(replacements)
    assert set(first)==set(last)==set(new_ids)
    assert not {r['item_id'] for r in kept}&set(parent_ids)
    selected=kept+replacements
    assert len(first_eventual(selected)[0])==len(first_eventual(original)[0])
    return selected,retired


def original_source(root,mid,spec,summary):
    kind=spec.get('serializer')
    if kind=='chat15' or mid=='microsoft/phi-4':relative='expansion_2026-10-15/attempts.jsonl'
    elif kind=='native15':relative='decision_refresh_2026-10-15/attempts.jsonl'
    elif kind=='native16':relative=f'additions_2026-10-16/{mid}/attempts.jsonl'
    elif kind=='native18':relative=f'native_additions_2026-10-18/{mid}/attempts.jsonl'
    elif kind=='chat16' or mid in ('haiku55','deepseek41flash'):relative=f'llm_additions_2026-10-16/{mid}/attempts.jsonl'
    elif kind in ('chat18','tev18'):relative=f'llm_additions_2026-10-18/{mid}/attempts.jsonl'
    else:raise AssertionError('Unmapped original source '+mid)
    requested=spec.get('model') or summary['models'][mid].get('model_requested') or mid
    attempts=[r for r in retest.rows(Path(root)/relative) if r.get('model_requested')==requested]
    assert len(first_eventual(attempts)[0])==1136,'Original source incomplete: '+mid
    return attempts,relative


def toronto_day(row):
    started=row.get('started') or {}
    if started.get('toronto'):return started['toronto'][:10]
    if started.get('utc'):
        return datetime.fromisoformat(started['utc'].replace('Z','+00:00')).astimezone(ZoneInfo('America/Toronto')).date().isoformat()
    return 'unreported'


def summarize(mid,spec,attempts,keys,metadata,selection,helpers,base=None):
    metrics,panels,panel_summary,quantiles,compliance=helpers
    native=spec['path'].endswith('/decisions') or spec['host']=='api.bespokelabs.ai'
    first,last=first_eventual(attempts);ff=list(first.values());ee=list(last.values())
    nn=[normalize(r,native) for r in ff];en=[normalize(r,native) for r in ee]
    assert len(nn)==len(keys)==1136
    primary=metrics(nn,keys);cost=monetary(attempts)
    value={'label':spec['label'],'model_requested':spec['model'],'provider_tag':spec['provider_tag'],
        'provider_name':spec['provider_name'],'route':'Bespoke direct' if spec['host']=='api.bespokelabs.ai' else 'OpenRouter',
        'condition':(base or {}).get('condition','corrected_questions_only'),
        'primary':primary,'eventual':metrics(en,keys),'recovery_attempts':len(attempts)-len(ff),
        'cost_all_attempts':cost,'cost_first_attempts':monetary(ff),
        'reported_api_cost_all_attempts':monetary(attempts,True),
        'cost_basis':'Selected recorded API charges or original captured accounted costs; only fresh direct Nimble cases use current captured tariff. Unreported costs remain unknown.',
        'known_usd_per_1000_questions':cost['known_usd']/1136*1000,
        'known_usd_per_primary_correct':cost['known_usd']/primary['correct'] if primary['correct'] else None,
        'latency_first_all':quantiles([float(a['latency_ms']) for a in ff]),
        'latency_first_usable':quantiles([float(a['latency_ms']) for a in ff if a['status']=='ok']),
        'latency_first_http200':quantiles([float(a['latency_ms']) for a in ff if a['http_status']==200]),
        'statuses_first':dict(Counter(a['status'] for a in ff)),
        'http_status_first':dict(Counter(str(a['http_status']) for a in ff)),
        'identities':dict(Counter(a.get('model_returned') or 'unreported (error)' for a in ff)),
        'providers_first':dict(Counter(a.get('provider') or spec['provider_name'] for a in ff)),
        'providers_all_attempts':dict(Counter(a.get('provider') or spec['provider_name'] for a in attempts)),
        'identities_all_attempts':dict(Counter(a.get('model_returned') or 'unreported (error)' for a in attempts)),
        'dates_toronto':dict(Counter(toronto_day(a) for a in ff)),
        'attempt_dates_toronto':dict(Counter(toronto_day(a) for a in attempts)),
        'panels':panel_summary(panels(nn,keys,selection)),
        'input_tokens_all_attempts':sum((a.get('usage') or {}).get('input_tokens',(a.get('usage') or {}).get('prompt_tokens',0)) or 0 for a in attempts),
        'output_tokens_all_attempts':sum((a.get('usage') or {}).get('output_tokens',(a.get('usage') or {}).get('completion_tokens',0)) or 0 for a in attempts),
        'reasoning_tokens_histogram':dict(Counter(str(a.get('reported_reasoning_tokens')) for a in ff)),
        'reasoning_text_present_count':sum(bool(a.get('reasoning_text_present')) for a in ff),
        'replacement_provenance':{'original_unchanged_cases':1134,'fresh_replacement_cases':2,
            'latency_pooling':'Pooled1134 original first-attempt latencies plus2 new first-attempt latencies; medians are not averaged',
            'route_changed_for_replacements':bool(spec.get('route_override'))}}
    for field in ('role','level'):
        value['by_'+field]={level:metrics([a for a in nn if metadata[a['item_id']][field]==level],keys)
                           for level in sorted({r[field] for r in metadata.values()})}
    if native:
        value['confidence']=[]
        for threshold in (.8,.9,.95):
            group=[r for r in nn if r['normalized_status']=='ok' and r['normalized_confidence'] is not None and r['normalized_confidence']>=threshold]
            value['confidence'].append({'threshold':threshold,'coverage':len(group)/1136,**metrics(group,keys)})
    else:value['finish_reasons']=dict(Counter(str(a.get('finish_reason')) for a in ff))
    if spec.get('route_override'):
        value['replacement_provenance'].update(original_route=spec['original_route'],new_route={k:spec[k] for k in ('provider_tag','provider_name','endpoint_name')},
            required_unchanged_dated_checkpoint=spec['required_unchanged_dated_checkpoint'])
    return value,nn,compliance(ff)


def read_csv(path):
    with Path(path).open(newline='',encoding='utf-8-sig') as stream:return list(csv.DictReader(stream))


def write_csv(path,records):
    buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    with Path(path).open('x',newline='',encoding='utf-8') as stream:stream.write(buf.getvalue())


def assemble(benchmark_root,key_path,retests=RETESTS,out=OUT):
    root,out,retests=Path(benchmark_root),Path(out),Path(retests)
    plan,candidates,mm=retest.load(root,retests)
    # Import scoring only in this offline process. Live runners never import it.
    from analysis_core import metrics,panels,panel_summary,correct,valid
    from matched_analysis import pairwise
    from score_expansion import load_key
    from text_models import quantiles
    from text_additions import compliance
    keys=load_key(key_path);original_summary=json.loads((root/retest.SUMMARY).read_text())
    assert len(original_summary['models'])==40 and original_summary['publication']['ranked_model_count']==37
    metadata=read_csv(root/'data/item_metadata.csv');selection=json.loads((root/'data/selection_manifest.json').read_text())
    original_bank=read_csv(root/'data/questions_1136.csv')
    repairs=json.loads((REPAIRS/'repair_design.json').read_text())['repairs']
    # Only old->new identity mapping is taken from private design. Its proposed
    # answer is not read or trusted: corrected key options inherit frozen key.
    repair_mapping=[{'parent_item_id':r['parent_item_id'],'new_item_id':r['new_item_id']} for r in repairs]
    bank,metadata,selection,newkeys,mapping=corrected_bank(original_bank,metadata,selection,candidates,repair_mapping,keys)
    assert len(bank)==1136 and sum(r['role']=='core' for r in metadata)==640
    md={r['item_id']:r for r in metadata};source_hashes={retest.SUMMARY:digest(root/retest.SUMMARY)}
    original_attempts={};old_success_verified=0
    for mid in original_summary['models']:
        spec=plan['models'].get(mid,{'model':original_summary['models'][mid].get('model_requested') or mid})
        aa,source=original_source(root,mid,spec,original_summary);source_hashes[source]=digest(root/source)
        native=spec.get('serializer','').startswith('native') or spec.get('serializer')=='tev18'
        first,last=first_eventual(aa)
        assert metrics([normalize(r,native) for r in first.values()],keys)==original_summary['models'][mid]['primary'],'Original primary reproduction failed: '+mid
        assert metrics([normalize(r,native) for r in last.values()],keys)==original_summary['models'][mid]['eventual'],'Original eventual reproduction failed: '+mid
        original_attempts[mid]=aa;old_success_verified+=1
    assert old_success_verified==40
    summary={'version':'corrected-two-wording-repairs-20261018-v1','status':'COMPLETE_CORRECTED_BANK_36_MODELS',
        'question_count':1136,'core_question_count':640,'model_count':36,'models':{},'by_family':[],
        'total_scored_model_questions':36*1136,'output_compliance':{},'sessions_utc':{},
        'original_evidence_validation':{'complete_original_primary_and_eventual_scores_reproduced':40,
                                      'original_summary_sha256':digest(root/retest.SUMMARY)},
        'publication':{'eligible_model_ids':[],'ranked_model_count':36,'ranked_model_question_cases':36*1136,
            'excluded_model_ids':['nimble_v4','microsoft/phi-4','haiku55','deepseek41flash'],
            'rule':'Only corrected full-bank continuous-model runs enter active rankings. Prior format exclusions remain previous-version diagnostics; old Nimble v4 is unavailable, not replaced by Max.'},
        'timing':'Pooled original1134 plus fresh2 full-body first-attempt latencies per model; mixed dates/routes explicitly recorded; not a fresh full-bank speed rerun',
        'replacement_ids':list(mapping.values()),'retired_parent_ids':list(mapping),
        'original_question_bank_sha256':digest(root/'data/questions_1136.csv'),
        'partial_models':{},'prior_version_format_diagnostics':{},'deltas':{}}
    model_rows={};selected_all=[];retired_all=[];private_sources={}
    helpers=(metrics,panels,panel_summary,quantiles,compliance)
    for mid,spec in plan['models'].items():
        original=original_attempts[mid]
        if mid=='nimble_v4':
            retained=[r for r in original if r['item_id'] not in mapping]
            retired_all.extend(r for r in original if r['item_id'] in mapping)
            first,last=first_eventual(retained)
            summary['partial_models'][mid]={'status':'ORIGINAL_MODEL_UNAVAILABLE','label':spec['label'],
                'reason':spec['blocked_reason'],'main_ranking_included':False,'full_bank_extrapolation':False,
                'planned':1136,'retained_unchanged_cases':1134,'missing_replacement_cases':2,
                'primary_on_retained_only':metrics([normalize(r,True) for r in first.values()],newkeys),
                'cost_recorded_retained_attempts':monetary(retained)}
            continue
        folder=retests/'models'/mid.replace('/','__')
        completion=json.loads((folder/'COMPLETED.json').read_text())
        assert completion['status']=='COMPLETE_TWO_CASES','Unreviewed retest: '+mid
        for name,expected in completion['files_sha256'].items():
            assert digest(folder/name)==expected,'Changed retest evidence: '+mid+'/'+name
            private_sources[str((folder/name).relative_to(retests))]=expected
        private_sources[str((folder/'COMPLETED.json').relative_to(retests))]=digest(folder/'COMPLETED.json')
        fresh=retest.rows(folder/'attempts.jsonl');assert all(not r.get('identity_issue') and r['status']!='unexpected_reasoning' for r in fresh)
        active,retired=select_replacements(original,fresh,set(mapping),set(mapping.values()))
        value,normalized,format_stats=summarize(mid,spec,active,newkeys,md,selection,helpers,original_summary['models'][mid])
        assert value['by_role']['core']['attempted']==640
        value['macro_family_accuracy']=sum(metrics([r for r in normalized if md[r['item_id']]['family_id']==fid],newkeys)['accuracy_attempted'] for fid in {m['family_id'] for m in metadata})/25
        summary['models'][mid]=value;summary['output_compliance'][mid]=format_stats;model_rows[mid]=normalized
        assert format_stats['eligible_for_main_comparison'],'Corrected output noncompliance: '+mid
        started=[r['started']['utc'] for r in active if (r.get('started') or {}).get('utc')]
        ended=[r['completed']['utc'] for r in active if (r.get('completed') or {}).get('utc')]
        summary['sessions_utc'][mid]={'started':min(started),'completed':max(ended)}
        summary['deltas'][mid]={'old_correct':original_summary['models'][mid]['primary']['correct'],
            'corrected_correct':value['primary']['correct'],
            'correct_delta':value['primary']['correct']-original_summary['models'][mid]['primary']['correct']}
        selected_all.extend(active);retired_all.extend(retired)
    assert len(model_rows)==36
    for original_family in original_summary['by_family']:
        fid=original_family['family_id'];ids={i for i,r in md.items() if r['family_id']==fid}
        summary['by_family'].append({'family_id':fid,'family':original_family['family'],'n':len(ids),
            'models':{mid:metrics([r for r in rr if r['item_id'] in ids],newkeys) for mid,rr in model_rows.items()}})
    for mid in ('microsoft/phi-4','haiku55','deepseek41flash'):
        summary['prior_version_format_diagnostics'][mid]={'version':'ORIGINAL_UNCORRECTED_1136','corrected_full_run':False,
            'main_ranking_included':False,'original_aggregate':deepcopy(original_summary['models'][mid])}
    summary['pairwise']=[{'a':a,'b':b,**pairwise(model_rows[a],model_rows[b],newkeys)} for a,b in itertools.combinations(model_rows,2)]
    index={m:{r['item_id']:r for r in rr} for m,rr in model_rows.items()}
    shared=[i for i in md if all(valid(index[m][i]) for m in index)]
    none=sum(not any(correct(index[m][i],newkeys) for m in index) for i in md)
    summary.update(all_tested_models_answered=len(shared),none_of_tested_models_correct=none,
        accuracy_on_shared_answered={m:metrics([r for r in rr if r['item_id'] in shared],newkeys) for m,rr in model_rows.items()},
        total_selected_http_attempts=len(selected_all),total_selected_accounted_cost=monetary(selected_all),
        total_selected_reported_cost=monetary(selected_all,True),
        retirement_overhead={'scope':'Retired two-item original attempts for previous37 ranked models, including unavailable old Nimble v4; not in active score, latency or cost',
            'attempts':len(retired_all),'accounted_cost':monetary(retired_all),'reported_api_cost':monetary(retired_all,True)})
    summary['publication'].update(eligible_model_ids=list(model_rows),none_of_ranked_models_correct=none,
                                 ranked_accounted_cost=monetary(selected_all))
    source_hashes.update({name:digest(root/name) for name in ('data/questions_1136.csv','data/item_metadata.csv','data/selection_manifest.json',
                                                           'analysis_core.py','matched_analysis.py','score_expansion.py','text_models.py','text_additions.py')})
    summary['source_files_sha256']=source_hashes
    summary['private_retest_sources_sha256']=private_sources
    summary['private_retest_plan_sha256']=digest(retests/'frozen_plan.json')
    summary['assembler_sources_sha256']={name:digest(ROOT/name) for name in ('assemble_corrected.py','test_assemble_corrected.py')}
    out.mkdir(parents=True,exist_ok=True)
    write_csv(out/'questions_1136.csv',bank);write_csv(out/'item_metadata.csv',metadata)
    retest.save_new(out/'selection_manifest.json',selection)
    summary['questions_sha256']=digest(out/'questions_1136.csv')
    retest.save_new(out/'summary.json',summary)
    retest.save_new(out/'checksums.json',{p.name:digest(p) for p in sorted(out.iterdir()) if p.is_file()})
    return summary


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--benchmark-root',required=True,type=Path)
    parser.add_argument('--key',required=True,type=Path)
    parser.add_argument('--retests',type=Path,default=RETESTS)
    parser.add_argument('--out',type=Path,default=OUT)
    args=parser.parse_args();summary=assemble(args.benchmark_root,args.key,args.retests,args.out)
    print(json.dumps({'status':summary['status'],'model_count':summary['model_count'],'questions':1136,
        'original_scores_verified':40,'deltas':summary['deltas']},indent=2))


if __name__=='__main__':main()
