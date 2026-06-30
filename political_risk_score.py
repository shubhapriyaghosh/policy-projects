import csv
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data' / 'political_risk_indicators.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'political_risk_scorecard.md'
OUT.parent.mkdir(exist_ok=True)
rows=[]
with DATA.open() as f:
    for r in csv.DictReader(f):
        score = 0.45*float(r['impact']) + 0.40*float(r['probability']) + 0.15*float(r['value'])
        r['risk_score'] = round(score, 1)
        r['band'] = 'High' if score >= 70 else 'Medium' if score >= 55 else 'Low'
        rows.append(r)
rows.sort(key=lambda x: x['risk_score'], reverse=True)
md=['# Political Risk Early Warning Scorecard','','| Indicator | Trend | Score | Band | Recommended response |','|---|---|---:|---|---|']
for r in rows:
    response = 'War-room monitoring, counter-narrative and leadership engagement' if r['band']=='High' else 'Weekly monitoring and field validation' if r['band']=='Medium' else 'Track monthly'
    md.append(f"| {r['indicator']} | {r['trend']} | {r['risk_score']} | {r['band']} | {response} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
