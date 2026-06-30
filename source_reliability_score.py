import csv
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data' / 'source_reliability_sample.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'source_reliability_scorecard.md'
OUT.parent.mkdir(exist_ok=True)
rows=[]
with DATA.open() as f:
    for r in csv.DictReader(f):
        score = 0.35*float(r['credibility']) + 0.25*float(r['timeliness']) + 0.25*float(r['corroboration']) + 0.15*(100-float(r['bias_risk']))
        r['confidence_score'] = round(score,1)
        r['confidence_band'] = 'High' if score >= 75 else 'Medium' if score >= 55 else 'Low'
        rows.append(r)
rows.sort(key=lambda x: x['confidence_score'], reverse=True)
md=['# OSINT Source Reliability Scorecard','','| Source | Confidence Score | Band | Use in brief |','|---|---:|---|---|']
for r in rows:
    use = 'Can support key judgment' if r['confidence_band']=='High' else 'Use only with corroboration' if r['confidence_band']=='Medium' else 'Do not use for key judgment without verification'
    md.append(f"| {r['source']} | {r['confidence_score']} | {r['confidence_band']} | {use} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
