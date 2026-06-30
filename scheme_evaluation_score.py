import csv
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data' / 'scheme_evaluation_sample.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'scheme_evaluation_scorecard.md'
OUT.parent.mkdir(exist_ok=True)
rows=[]
with DATA.open() as f:
    for r in csv.DictReader(f):
        reach_rate = 100*float(r['actual_reached'])/float(r['target_beneficiaries'])
        cost_eff = max(0, 100 - float(r['cost_lakh'])/5)
        score = 0.35*float(r['outcome_score']) + 0.25*reach_rate + 0.15*cost_eff + 0.15*float(r['citizen_awareness']) + 0.10*(100-float(r['leakage_risk']))
        r['evaluation_score'] = round(score,1)
        r['reach_rate'] = round(reach_rate,1)
        rows.append(r)
rows.sort(key=lambda x: x['evaluation_score'], reverse=True)
md=['# Scheme Evaluation Scorecard','','| Scheme | Reach Rate | Evaluation Score | Decision |','|---|---:|---:|---|']
for r in rows:
    decision = 'Scale with monitoring' if r['evaluation_score'] >= 70 else 'Redesign before scaling' if r['evaluation_score'] >= 55 else 'Pause and diagnose'
    md.append(f"| {r['scheme']} | {r['reach_rate']}% | {r['evaluation_score']} | {decision} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
