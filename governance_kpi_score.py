import csv
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data' / 'governance_kpi_sample.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'governance_kpi_scorecard.md'
OUT.parent.mkdir(exist_ok=True)
rows=[]
with DATA.open() as f:
    for r in csv.DictReader(f):
        score = 0.35*float(r['sla_met_pct']) + 0.25*(100-min(float(r['avg_tat_days'])*4,100)) + 0.20*(float(r['citizen_score'])*20) + 0.10*(100-float(r['reopen_rate_pct'])*5) + 0.10*(100-min(float(r['grievances'])/4,100))
        r['governance_score'] = round(score,1)
        r['risk_band'] = 'Critical' if score < 55 else 'Watch' if score < 70 else 'Healthy'
        rows.append(r)
rows.sort(key=lambda x: x['governance_score'])
md=['# Governance KPI Scorecard','','| Department | Score | Band | Key intervention |','|---|---:|---|---|']
for r in rows:
    action = 'SLA redesign, triage automation, escalation dashboard' if r['risk_band']=='Critical' else 'Improve reopen controls and citizen feedback loop' if r['risk_band']=='Watch' else 'Maintain and scale best practice'
    md.append(f"| {r['department']} | {r['governance_score']} | {r['risk_band']} | {action} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
