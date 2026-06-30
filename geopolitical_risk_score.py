import csv
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data' / 'security_events_sample.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'security_event_risk_scorecard.md'
OUT.parent.mkdir(exist_ok=True)
rows=[]
with DATA.open() as f:
    for r in csv.DictReader(f):
        score = 0.25*float(r['severity']) + 0.20*float(r['probability']) + 0.15*float(r['source_reliability']) + 0.25*float(r['business_impact']) + 0.15*float(r['escalation_signal'])
        r['risk_score'] = round(score,1)
        r['band'] = 'High' if score >= 75 else 'Medium' if score >= 60 else 'Low'
        rows.append(r)
rows.sort(key=lambda x: x['risk_score'], reverse=True)
md=['# Security Event Risk Scorecard','','| Event | Region | Type | Score | Band | Analyst note |','|---|---|---|---:|---|---|']
for r in rows:
    note = 'Immediate executive monitoring required' if r['band']=='High' else 'Monitor and corroborate with additional sources' if r['band']=='Medium' else 'Low-intensity tracking'
    md.append(f"| {r['event_id']} | {r['region']} | {r['event_type']} | {r['risk_score']} | {r['band']} | {note} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
