#!/usr/bin/env python3
"""Resume after a returned transient API error wrapped inside HTTP 200.

Never alters or repeats recorded attempts. Identity checks still apply to every
response that contains choices. Request parameters, timers and scoring are the
unchanged frozen runner. The sole guard exception is a no-choice transient
error envelope, which remains an unsuccessful attempt.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path

import field_runner as f


def transient_envelope(record):
    raw=record.get('raw_response') or {}
    return (record['http_status']==200 and not raw.get('choices')
            and isinstance(raw.get('error'),dict)
            and raw['error'].get('code') in f.run.transport.TRANSIENT)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model',choices=f.CONFIG,required=True)
    parser.add_argument('--execute',action='store_true')
    args=parser.parse_args()
    f.args=argparse.Namespace(model=args.model,waves=0,execute=args.execute)
    f.configure(args.model)
    r=f.run
    original=r.check_identity
    def guarded(record):
        if transient_envelope(record):
            return
        original(record)
    r.check_identity=guarded
    if not args.execute:
        print('DRY_RUN: no reconciliation or API calls')
        raise SystemExit(0)
    attempts=r.chat.rows(r.OUT/'attempts.jsonl')
    dispatches=r.chat.rows(r.OUT/'dispatches.jsonl')
    results=r.chat.rows(r.OUT/'results.jsonl')
    signature=lambda a:(a['request_index'],a['attempt'])
    assert {signature(a) for a in attempts}=={signature(a) for a in dispatches},'Unresolved dispatch: never repeat an uncertain billed call'
    for a in attempts:
        guarded(a)
    missing={a['request_index'] for a in attempts}-{a['request_index'] for a in results}
    _,plan=r.prepare()
    indexed={p['request_index']:p for p in plan}
    receipt=r.OUT/'continuation_receipt.json'
    r.transport.save_bound(receipt,{
        'time':r.transport.timestamps(),
        'reason':'HTTP 200 containing transient upstream error with no choices has no model/provider identity to attest.',
        'source_sha256':sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_path':str(Path(__file__).relative_to(r.ROOT)),
        'existing_attempts_prefix_bytes':(r.OUT/'attempts.jsonl').stat().st_size,
        'existing_attempts_prefix_sha256':sha256((r.OUT/'attempts.jsonl').read_bytes()).hexdigest(),
        'reconciled_case_indices':sorted(missing),
        'request_or_timer_or_scoring_changes':False,
        'policy':'All recorded attempts retained. No existing attempt replayed. No extra recovery for the HTTP-200 envelope; it remains unsuccessful under the original parser.'})
    for index in sorted(missing):
        group=sorted([a for a in attempts if a['request_index']==index],key=lambda a:a['attempt'])
        assert any(transient_envelope(a) for a in group),'Only this explained guard failure can be reconciled here'
        r.transport.append(r.OUT/'results.jsonl',{**indexed[index],
            'first_status':group[0]['status'],'eventual_status':group[-1]['status'],
            'attempts':len(group),'item_elapsed_ms':None,
            'terminal_reconciled_without_replay':True})
    r.execute(f.args)
