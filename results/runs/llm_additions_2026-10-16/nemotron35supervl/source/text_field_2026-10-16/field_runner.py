#!/usr/bin/env python3
"""Seven answer-blind text additions using the unchanged Lightning transport.

Each model runs in its own process with two concurrent requests. Provider pins,
no-reasoning contract, bank and software are bound before paid full execution.
"""
import argparse
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys
import urllib.request

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[1]
SOURCE = ROOT/'runs/nemotron_2026-10-16/runner.py'
spec = importlib.util.spec_from_file_location('nemotron_protocol',SOURCE)
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)
CONFIG = {
    'haiku55':('Claude Haiku 5.5','anthropic/claude-haiku-5.5','anthropic','Anthropic','anthropic/claude-haiku-5.5-20261007'),
    'glm53flash':('GLM 5.3 Flash','z-ai/glm-5.3-flash','deepinfra/fp4','DeepInfra','z-ai/glm-5.3-flash-20260826'),
    'glm47flash':('GLM 4.7 Flash','z-ai/glm-4.7-flash','cloudflare','Cloudflare','z-ai/glm-4.7-flash-20260119'),
    'deepseek41flash':('DeepSeek V4.1 Flash','deepseek/deepseek-v4.1-flash','deepinfra/fp8','DeepInfra','deepseek/deepseek-v4.1-flash-20260910'),
    'mimo26flash':('MiMo V2.6 Flash','xiaomi/mimo-v2.6-flash','xiaomi/fp8','Xiaomi','xiaomi/mimo-v2.6-flash-20260921'),
    'qwen38flash':('Qwen3.8 Flash','qwen/qwen3.8-flash','alibaba/us-east-1','Alibaba','qwen/qwen3.8-flash-20260826'),
    'tencenthy3':('Tencent Hy3','tencent/hy3','tencent/fp8','Tencent','tencent/hy3-20260706'),
    'nemotron35supervl':('Nemotron 3.5 Super VL','nvidia/nemotron-3.5-super-vl','crusoe/bf16','Crusoe','nvidia/nemotron-3.5-super-vl-20261015'),
}


def configure(model_id):
    label,model,tag,provider,snapshot = CONFIG[model_id]
    run.OUT = BASE/model_id
    run.OUT.mkdir(parents=True,exist_ok=True)
    run.MODEL,run.TAG,run.PROVIDER,run.SNAPSHOT = model,tag,provider,snapshot
    run.GUARD = .25
    return label


def freeze(plan):
    run.transport.save_bound(run.OUT/'manifest.json',{
        'version':'seven-field-additions-20261016-v1','label':CONFIG[args.model][0],
        'model_id':args.model,'model_requested':run.MODEL,'provider_tag':run.TAG,
        'provider_name':run.PROVIDER,'required_metadata_snapshot':run.SNAPSHOT,
        'endpoint':'https://openrouter.ai'+run.PATH,'question_count':1136,
        'questions_sha256':sha256((ROOT/'data/questions_1136.csv').read_bytes()).hexdigest(),
        'question_order':'Exact saved eight-LLM bank order',
        'prompt':'Exact frozen prompt_text plus original numeric-ID-only suffix; no key or answer feedback',
        'max_tokens':16,'stream':False,'reasoning':{'enabled':False},
        'temperature':'Omitted, matching original eight regular LLM benchmark runs',
        'concurrency':{'maximum_per_model':2,'questions_per_wave':2,'barrier':'Each model independently waits for its two cases; at most 14 requests globally'},
        'timing':'Unmodified decision_refresh.send, new HTTPS connection, connect through full response JSON body; local preparation, queue and retry wait excluded',
        'connect_timeout_seconds':10,'total_response_timeout_seconds':90,
        'retry':'At most one retry for transport failure or HTTP 408/429/5xx, never for invalid output or wrong answers',
        'primary':'First attempts, denominator 1136, failures unsuccessful; recovery separate',
        'compatibility_probes':'Separate from full run and never substituted into primary results',
        'identity_limit':'Provider pinned and metadata dated snapshot captured; an alias response is not independent checkpoint attestation',
        'known_spend_guard_usd':run.GUARD,'guard_limit':'Soft before-dispatch guard, unknown and in-flight charges not a hard billing cap',
        'request_plan':plan})
    sources=[SOURCE,SOURCE.with_name('test_runner.py'),Path(__file__),BASE/'test_field_runner.py',ROOT/'decision_refresh.py',ROOT/'text_models.py',ROOT/'run_benchmark.py']
    run.transport.save_bound(run.OUT/'software.json',{str(p.relative_to(ROOT)):sha256(p.read_bytes()).hexdigest() for p in sources})


def metadata():
    path=run.OUT/'model_metadata.json'
    if path.exists():
        return
    url='https://openrouter.ai/api/v1/models/'+run.MODEL+'/endpoints'
    with urllib.request.urlopen(url,context=run.transport.ssl.create_default_context(cafile='/etc/ssl/cert.pem'),timeout=30) as response:
        data=json.load(response)['data']
    selected=[e for e in data['endpoints'] if e['tag']==run.TAG and e.get('status')==0 and not e.get('service_tier')]
    assert len(selected)==1 and run.SNAPSHOT in selected[0]['name']
    e=selected[0]
    assert e['provider_name']==run.PROVIDER
    assert float(e['pricing']['prompt'])*1e6 <= .2 and float(e['pricing']['completion'])*1e6 <= .8
    assert {'reasoning','max_tokens'} <= set(e['supported_parameters'])
    run.transport.save_bound(path,{'retrieved':run.transport.timestamps(),'url':url,'data':data})


def probe():
    metadata()
    path=run.OUT/('compatibility_probe_retry.json' if args.probe_retry else 'compatibility_probe.json')
    if args.probe_retry:
        previous=json.loads((run.OUT/'compatibility_probe.json').read_text())
        assert previous['transport_failure'] or previous['http_status'] in run.transport.TRANSIENT
    assert not path.exists(),'Refusing to replay completed compatibility probe'
    questions,plan=run.prepare()
    task=plan[0]
    body=run.transport.canonical(run.payload(questions[task['item_id']]))
    key=run.transport.api_key(ROOT.parent/'jev/.env')
    response=run.transport.send(body,key)
    record={**task,'attempt':1,**response,**run.parse(response)}
    run.transport.save_bound(path,record)
    print(json.dumps({'model_id':args.model,'http_status':record['http_status'],
          'status':record['status'],'finish_reason':record['finish_reason'],
          'reasoning_tokens':record['reported_reasoning_tokens'],
          'reasoning_text':record['reasoning_text_present'],'cost':record['reported_cost_usd'],
          'error':record['error'],'raw_error':record['raw_response'].get('error',{}).get('message'),
          'output':record['output_text'],'latency_ms':record['latency_ms']}),flush=True)


run.freeze=freeze
run.metadata=metadata


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',choices=CONFIG,required=True)
    parser.add_argument('--probe',action='store_true')
    parser.add_argument('--probe-retry',action='store_true')
    parser.add_argument('--execute',action='store_true')
    parser.add_argument('--validate',action='store_true')
    parser.add_argument('--waves',type=int,default=0)
    args=parser.parse_args()
    configure(args.model)
    if args.probe or args.probe_retry:
        probe()
    elif args.validate:
        run.validate()
    else:
        if args.execute:
            probe_path=run.OUT/'compatibility_probe_retry.json'
            if not probe_path.exists():
                probe_path=run.OUT/'compatibility_probe.json'
            result=json.loads(probe_path.read_text())
            assert result['status']=='ok','Compatibility probe did not confirm a usable no-reasoning answer'
            run.check_identity(result)
        run.execute(args)
