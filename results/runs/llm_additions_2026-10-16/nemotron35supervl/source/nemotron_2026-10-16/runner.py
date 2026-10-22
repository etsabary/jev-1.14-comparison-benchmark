#!/usr/bin/env python3
"""Answer-blind 1,136-question Nemotron text run, dry-run unless --execute.

Preserves all published benchmark evidence. Uses the exact existing chat prompt
and full-response HTTPS timer. Pilot calls are excluded; no key is read here.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from hashlib import sha256
import json
import math
from pathlib import Path
import sys
import threading
import time
import urllib.request

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
sys.path.insert(0, str(ROOT))
import decision_refresh as transport
import text_models as chat

MODEL = 'nvidia/nemotron-3.5-lightning'
TAG = 'coreweave/bf16'
PROVIDER = 'CoreWeave'
SNAPSHOT = 'nvidia/nemotron-3.5-lightning-20260807'
PATH = '/api/v1/chat/completions'
GUARD = .15
transport.PATH = PATH


def payload(question):
    return {'model': MODEL,
            'messages': [{'role': 'user', 'content': question['prompt_text']+chat.SUFFIX}],
            'max_tokens': 16, 'stream': False, 'usage': {'include': True},
            'provider': {'only': [TAG], 'allow_fallbacks': False, 'require_parameters': True},
            'reasoning': {'enabled': False}}


def parse(response):
    result = chat.parse(response)
    if result['reasoning_text_present'] or result['reported_reasoning_tokens'] not in (None, 0):
        result['status'] = 'unexpected_reasoning'
        result['choice'] = None
    return result


def check_identity(record):
    if record['http_status'] == 200 and not record['error']:
        assert record['provider'] == PROVIDER, 'Unexpected provider'
        assert record['model_returned'] in (MODEL, SNAPSHOT), 'Unexpected model identity'
        assert record['reported_cost_usd'] is not None, 'Missing HTTP-success cost'
        assert not record['reasoning_text_present'], 'Unexpected reasoning text'
        assert record['reported_reasoning_tokens'] in (None, 0), 'Unexpected reasoning tokens'


def prepare():
    questions = transport.read_csv(ROOT/'data/questions_1136.csv')
    bound = json.loads((ROOT/'data/baseline_reference_manifest.json').read_text())
    assert sha256((ROOT/'data/questions_1136.csv').read_bytes()).hexdigest() == bound['questions_sha256']
    indexed = {q['item_id']: q for q in questions}
    assert len(questions) == len(indexed) == 1136
    order = list(dict.fromkeys(p['item_id'] for p in chat.rows(ROOT/'expansion_2026-10-15/request_plan.jsonl')))
    assert set(order) == set(indexed) and len(order) == 1136
    plan = []
    for position, item_id in enumerate(order):
        q = indexed[item_id]
        content = {k: q[k] for k in ('instructions', 'context', 'question')}
        content['options'] = [q[f'option_{i}'] for i in range(1,6)]
        assert transport.digest(content) == q['prompt_sha256']
        body = payload(q)
        plan.append({'request_index': position+1, 'item_id': item_id,
                     'wave': position//2+1, 'model_requested': MODEL,
                     'prompt_sha256': q['prompt_sha256'], 'message_sha256': transport.digest(body['messages']),
                     'request_payload_sha256': transport.digest(body),
                     'request_body_bytes': len(transport.canonical(body))})
    return indexed, plan


def freeze(plan):
    transport.save_bound(OUT/'manifest.json', {
        'version':'nemotron-lightning-full-text-20261016-v1',
        'model_requested':MODEL, 'provider_tag':TAG, 'provider_name':PROVIDER,
        'required_metadata_snapshot':SNAPSHOT, 'endpoint':'https://openrouter.ai'+PATH,
        'questions_sha256':sha256((ROOT/'data/questions_1136.csv').read_bytes()).hexdigest(),
        'question_count':1136, 'question_order':'Exact saved eight-LLM bank order',
        'prompt':'Exact frozen prompt_text plus original numeric-ID-only suffix; no key or answer feedback',
        'max_tokens':16, 'stream':False, 'reasoning':{'enabled':False},
        'temperature':'Omitted, matching original eight regular LLM benchmark runs',
        'concurrency':{'maximum':2, 'questions_per_wave':2, 'barrier':'Both cases settle before next wave'},
        'timing':'Unmodified decision_refresh.send transport, with chat-completions path; new HTTPS connection, connect through full response JSON body; preparation, local queue and retry wait excluded',
        'connect_timeout_seconds':10, 'total_response_timeout_seconds':90,
        'retry':'At most one retry for transport failure or HTTP 408/429/5xx; never for invalid output or wrong answers',
        'primary':'First attempts, denominator 1136, failures unsuccessful; recovery separate',
        'pilot_excluded':'All 25 earlier pilot questions rerun under full protocol; pilot used temperature=0 and is not merged or substituted',
        'identity_limit':'Provider pinned; dated snapshot captured in endpoint metadata. Response model may be alias, not independent checkpoint attestation.',
        'known_spend_guard_usd':GUARD, 'guard_limit':'Soft stop before dispatch, not hard cap on unknown/in-flight charges',
        'request_plan':plan})
    sources = [Path(__file__), OUT/'test_runner.py', ROOT/'decision_refresh.py', ROOT/'text_models.py', ROOT/'run_benchmark.py']
    transport.save_bound(OUT/'software.json', {str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sources})


def metadata():
    if (OUT/'model_metadata.json').exists():
        return
    url = 'https://openrouter.ai/api/v1/models/'+MODEL+'/endpoints'
    with urllib.request.urlopen(url, context=transport.ssl.create_default_context(cafile='/etc/ssl/cert.pem'), timeout=30) as response:
        data = json.load(response)['data']
    matches = [e for e in data['endpoints'] if e['tag'] == TAG and e.get('status') == 0 and not e.get('service_tier')]
    assert len(matches) == 1 and SNAPSHOT in matches[0]['name']
    e = matches[0]
    assert e['provider_name'] == PROVIDER and e['quantization'] == 'bf16'
    assert float(e['pricing']['prompt'])*1e6 <= .1 and float(e['pricing']['completion'])*1e6 <= .5
    assert {'reasoning','max_tokens'} <= set(e['supported_parameters'])
    transport.save_bound(OUT/'model_metadata.json', {'retrieved':transport.timestamps(), 'url':url, 'data':data})


def validate():
    questions, plan = prepare()
    manifest = json.loads((OUT/'manifest.json').read_text())
    assert manifest['request_plan'] == plan
    for name, expected in json.loads((OUT/'software.json').read_text()).items():
        assert sha256((ROOT/name).read_bytes()).hexdigest() == expected, name
    attempts, results = chat.rows(OUT/'attempts.jsonl'), chat.rows(OUT/'results.jsonl')
    dispatches = chat.rows(OUT/'dispatches.jsonl')
    done = transport.reconcile(dispatches, attempts, results, plan)
    by_index = {p['request_index']:p for p in plan}
    for a in attempts:
        assert all(a[k] == v for k,v in by_index[a['request_index']].items())
        for name, expected in parse(a).items():
            assert a[name] == expected, name
        check_identity(a)
    first, eventual = chat.first_and_eventual(attempts)
    assert len(done) == 1136
    for r in results:
        i = r['request_index']
        assert r['first_status'] == first[i]['status']
        assert r['eventual_status'] == eventual[i]['status']
        assert r['attempts'] == eventual[i]['attempt']
    completion = json.loads((OUT/'completion.json').read_text())
    assert completion['status'] == 'COMPLETE_1136'
    for name, expected in completion['files_sha256'].items():
        assert sha256((OUT/name).read_bytes()).hexdigest() == expected, name
    print('PASS: complete 1136, original exact inputs, immutable source/plan, dispatch reconciliation, strict parser, no reasoning, pinned identity, usage and checksum validation; no API call or answer key')
    return first, eventual, attempts


def execute(args):
    questions, plan = prepare()
    if not args.execute:
        print(json.dumps({'mode':'DRY_RUN','planned':len(plan),'paid_calls':0,'model':MODEL,
                          'provider':TAG,'max_tokens':16,'reasoning_enabled':False,
                          'pilot_questions_in_primary':0}))
        return
    freeze(plan)
    metadata()
    key = transport.api_key(ROOT.parent/'jev/.env')
    assert key
    attempts = chat.rows(OUT/'attempts.jsonl') if (OUT/'attempts.jsonl').exists() else []
    results = chat.rows(OUT/'results.jsonl') if (OUT/'results.jsonl').exists() else []
    dispatches = chat.rows(OUT/'dispatches.jsonl') if (OUT/'dispatches.jsonl').exists() else []
    done = transport.reconcile(dispatches, attempts, results, plan)
    for record in attempts:
        check_identity(record)
    lock, halt = threading.Lock(), threading.Event()
    def one(task):
        assert transport.PATH == PATH
        body = transport.canonical(payload(questions[task['item_id']]))
        assert sha256(body).hexdigest() == task['request_payload_sha256']
        collected, start = [], time.perf_counter()
        try:
            for attempt in (1,2):
                with lock:
                    if halt.is_set():
                        if collected:
                            break
                        return
                    assert math.fsum(a['reported_cost_usd'] or 0 for a in attempts) < GUARD, 'Known spend guard reached'
                    transport.append(OUT/'dispatches.jsonl',{**task,'attempt':attempt,'dispatch':transport.timestamps()})
                response = transport.send(body,key)
                record = {**task,'attempt':attempt,**response,**parse(response)}
                with lock:
                    transport.append(OUT/'attempts.jsonl',record)
                    attempts.append(record)
                collected.append(record)
                check_identity(record)
                if attempt == 1 and (record['transport_failure'] or record['http_status'] in transport.TRANSIENT):
                    wait = transport.retry_wait(response)
                    with lock:
                        transport.append(OUT/'retry_waits.jsonl',{'request_index':task['request_index'],'seconds':wait})
                    if halt.wait(wait):
                        break
                    continue
                break
            with lock:
                terminal = {**task,'first_status':collected[0]['status'], 'eventual_status':collected[-1]['status'],
                            'attempts':len(collected),'item_elapsed_ms':(time.perf_counter()-start)*1000}
                transport.append(OUT/'results.jsonl',terminal)
                results.append(terminal)
                if collected[-1]['http_status'] in (400,401,402,403,404,413,422):
                    raise ValueError('Client rejection; stop for inspection')
        except Exception:
            halt.set()
            raise
    completed_waves = 0
    with ThreadPoolExecutor(max_workers=2) as pool:
        for wave in sorted({p['wave'] for p in plan if p['request_index'] not in done}):
            todo = [p for p in plan if p['wave']==wave and p['request_index'] not in done]
            errors = []
            for future in as_completed([pool.submit(one,t) for t in todo]):
                try:
                    future.result()
                except Exception as exc:
                    errors.append(type(exc).__name__+': '+str(exc))
            progress = {'wave':wave,'completed_cases':len(results),'attempts':len(attempts),
                        'known_cost_usd':math.fsum(a['reported_cost_usd'] or 0 for a in attempts),
                        'missing_cost_attempts':sum(a['reported_cost_usd'] is None for a in attempts),
                        'first_status_counts':dict(Counter(r['first_status'] for r in results)),
                        'time':transport.timestamps()}
            transport.append(OUT/'progress.jsonl',progress)
            if wave % 25 == 0 or errors or len(results)==1136:
                print(json.dumps(progress),flush=True)
            if errors:
                raise ValueError('; '.join(errors))
            completed_waves += 1
            if args.waves and completed_waves >= args.waves:
                print(json.dumps(progress),flush=True)
                return
    assert len(results) == 1136
    names = ['manifest.json','software.json','model_metadata.json','dispatches.jsonl','attempts.jsonl','results.jsonl']
    transport.save_bound(OUT/'completion.json',{'status':'COMPLETE_1136','completed':transport.timestamps(),
        'files_sha256':{n:sha256((OUT/n).read_bytes()).hexdigest() for n in names}})
    validate()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--validate',action='store_true')
    parser.add_argument('--waves',type=int,default=0)
    args = parser.parse_args()
    if args.validate:
        validate()
    else:
        execute(args)
