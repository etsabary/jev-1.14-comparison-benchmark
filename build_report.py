"""Generate the expanded README and Pages site from fixed aggregate evidence."""
import json
from pathlib import Path
import re
import shutil
import markdown

ROOT=Path(__file__).resolve().parent
REPO='https://github.com/etsabary/jev-1.14-comparison-benchmark'


def table(headers, rows):
    return '| '+' | '.join(headers)+' |\n|'+ '|'.join(['---']+['---:']*(len(headers)-1))+'|\n'+''.join('| '+' | '.join(str(v) for v in row)+' |\n' for row in rows)+'\n'


def pct(n,d):return f'{100*n/d:.1f}%' if d else 'n/a'


def render(text,title):
    body=markdown.markdown(text,extensions=['tables','fenced_code','toc'])
    pages={'THREE_MODEL_REFERENCE.md':'three_model_reference.html','FUNCTIONS.md':'functions.html','README.md':'index.html'}
    body=re.sub(r'href="(?!https?://|#)([^"]+)"',lambda m:'href="'+pages.get(m[1],REPO+'/blob/main/'+m[1])+'"',body)
    return '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'''+title+'''</title><style>body{max-width:1260px;margin:auto;padding:32px 24px 80px;background:#f8fafc;color:#193047;font:17px/1.65 system-ui,sans-serif}h1{font-size:2.35rem;line-height:1.2}h2{margin-top:2.3rem;line-height:1.3}a{color:#087f8c}img{max-width:100%;height:auto;background:white;border-radius:10px}table{display:block;overflow-x:auto;max-width:100%;border-collapse:collapse;font-size:.86rem;margin:20px 0}th,td{border-bottom:1px solid #d5dfe9;padding:9px 11px;text-align:left;vertical-align:top}th{background:#e6eef5}code{font-size:.85em;overflow-wrap:anywhere}pre{overflow:auto;background:#e6eef5;padding:16px}nav{display:flex;gap:18px;flex-wrap:wrap;border-bottom:1px solid #d5dfe9;padding-bottom:16px;font-size:.9rem}p{max-width:100ch}</style></head><body><nav><a href="index.html">Eleven-model comparison</a><a href="functions.html">Functions and load</a><a href="three_model_reference.html">Original three-model reference</a><a href="'''+REPO+'">Repository and evidence</a></nav><main>'+body+'</main></body></html>\n'


def build():
    s=json.loads((ROOT/'expansion_2026-10-15/summary.json').read_text())
    old=json.loads((ROOT/'analysis/summary.json').read_text())
    models=s['models'];historical={'jev113','jev114','luna_decisions'}
    order=sorted(models,key=lambda m:-models[m]['primary']['correct'])
    parts={}
    rr=[]
    for m in order:
        d=models[m];p=d['primary']
        timing=s['historical_speeds'][m]['full_bank_saved_latency_all_outcomes'] if m in historical else d['latency_first_all']
        assert timing['n']==1136
        rr.append([d['label'],p['correct'],pct(p['correct'],1136),f"{d['by_role']['core']['correct']}/640",p['wrong'],p['unanswered'],f"{timing['median_ms']:.0f} ms"+(' historical' if m in historical else ''),f"{timing['p95_ms']:.0f} ms"])
    parts['RESULTS']=table(['Model','Correct / 1,136','Accuracy','Core correct','Wrong valid','Unanswered','Full-bank median','p95'],rr)
    rr=[]
    for m in order:
        if m in historical:continue
        d=models[m];c=d['cost_all_attempts']
        rr.append([d['label'],f"${c['known_usd']:.8f}",f"${d['known_usd_per_1000_questions']:.8f}",c['missing_attempts']])
    parts['COSTS']=table(['Model','Known cost for 1,136','Normalized cost per 1,000','Attempts missing cost'],rr)
    rr=[]
    for m in ['jev113','jev114','luna_decisions']:
        h=s['historical_speeds'][m]
        for f,label in [('original_1000_saved_latency','Original 1,000-question cohort'),('original_1000_openrouter_subset','Original OpenRouter-only subset'),('saved_successful_latency_all_records','All successful bank outcomes'),('shared_136_extension_saved_latency','Shared 136-question extension')]:
            if f in h:
                q=h[f];rr.append([models[m]['label'],label,q['n'],f"{q['median_ms']:.1f} ms",f"{q['p95_ms']:.1f} ms"])
    parts['HISTORICAL_SPEEDS']=table(['Model','Supporting historical cohort','Timed outcomes','Median','p95'],rr)
    rr=[]
    for m in order:
        p=models[m]['panels']
        rr.append([models[m]['label'],f"{p['rotation']['all_correct']}/25",f"{p['rotation']['consistent']}/{p['rotation']['complete']}",f"{p['contrast']['both_correct']}/25",f"{p['candidate_checks']['correct']}/80",f"{p['candidate_checks']['all_checks_correct']}/16"])
    parts['PANELS']=table(['Model','All rotations correct','Consistent / complete panels','Both evidence answers correct','Candidate checks correct','All five checks correct'],rr)
    rr=[]
    for m in order:
        if m in historical:continue
        d=models[m];rr.append([d['label'],d['primary']['correct'],d['format_sensitivity_POSTHOC']['leading_id_correct'],d['statuses_first'].get('invalid_output',0),d['statuses_first'].get('http_failure',0),d['recovery_attempts'],d['eventual']['correct']])
    parts['FORMAT']=table(['Model','Strict correct','Leading-ID correct','Invalid first output','First transport/HTTP failures','Recovery attempts','Eventual correct'],rr)
    rr=[]
    for cutoff in [.8,.9,.95]:
        cells=[]
        for m in ['jev113','jev114','luna']:
            d=next(x for x in old['confidence'][m] if x['threshold']==cutoff)
            cells.append(f"{d['correct']}/{d['attempted']} ({pct(d['correct'],d['attempted'])}; {pct(d['attempted'],1136)} coverage)")
        rr.append([f'≥{cutoff:g}',*cells])
    parts['CONFIDENCE']=table(['Confidence cutoff','Jev 1.13','Jev 1.14','Luna Decisions'],rr)
    parts['IDENTITIES']=table(['Service','Returned identities and counts','Backend tag','Toronto dates'],[[models[m]['label'],'; '.join('`'+k+'` ('+str(v)+')' for k,v in models[m]['identities'].items()),models[m].get('provider_tag','historical routes retained'),', '.join(models[m]['dates_toronto'])] for m in order])
    parts['ANALYSIS']=(ROOT/'report_sections.md').read_text()
    companion=json.loads((ROOT/'expansion_2026-10-15/companion_images.json').read_text())
    names={'typesafe/jev-1.14':'Jev 1.14','openai/gpt-6-luna-decisions':'Luna Decisions','openai/gpt-6-luna':'Luna regular','openai/gpt-5.4-nano':'GPT-5.4 nano','google/gemini-2.5-flash-lite':'Gemini 2.5 Flash-Lite'}
    parts['IMAGES']=table(['Image configuration','Correct / 200','Accuracy','Median full reply','Known actual 200-question cost'],[[names[m],d['correct_first'],pct(d['correct_first'],200),f"{d['latency_first_all_ms']['median']:.0f} ms",f"${d['core_cost']['reported_usd']:.8f}"+('*' if d['core_cost']['missing_records'] else '')] for m,d in companion['models'].items()])+'\nAn asterisk marks missing error charges. Image costs here are actual 200-question amounts; the image repo’s per-1,000 chart remains a separately labelled normalization.\n'
    text=(ROOT/'report_layout.md').read_text()
    for key,value in parts.items():text=text.replace('{{'+key+'}}',value.rstrip())
    assert '{{' not in text
    (ROOT/'README.md').write_text(text)
    functions='# Results by function and load level\n\nThe [main report](README.md) explains the historical and new-run conditions. All cells below use strict primary results.\n\n'+(ROOT/'task_examples.md').read_text()+'\n## All 25 functions\n\n'
    functions+=table(['Function','n']+[models[m]['label'] for m in order],[[f['family'],f['n']]+[f"{f['models'][m]['correct']} ({pct(f['models'][m]['correct'],f['n'])})" for m in order] for f in s['by_family']])
    for field,heading in [('by_role','Core and related item types'),('by_level','Engineered load levels')]:
        functions+='## '+heading+'\n\n'
        functions+=table(['Group','n']+[models[m]['label'] for m in order],[[v,models[order[0]][field][v]['attempted']]+[f"{models[m][field][v]['correct']} ({pct(models[m][field][v]['correct'],models[m][field][v]['attempted'])})" for m in order] for v in models[order[0]][field]])
    (ROOT/'FUNCTIONS.md').write_text(functions.rstrip()+'\n')
    for p in (ROOT/'figures').glob('*'):shutil.copyfile(p,ROOT/'docs/figures'/p.name)
    (ROOT/'docs/index.html').write_text(render(text,'Eleven models on 1136 text decisions'))
    (ROOT/'docs/functions.html').write_text(render(functions,'Text decision results by function and load'))
    print('Built expanded README, function tables and Pages; original report preserved')


if __name__=='__main__':build()
