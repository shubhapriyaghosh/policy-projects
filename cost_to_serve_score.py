import csv
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data' / 'cost_to_serve_sample.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'cost_to_serve_diagnostic.md'
OUT.parent.mkdir(exist_ok=True)
rows=[]
with DATA.open() as f:
    for r in csv.DictReader(f):
        pain = 0.30*float(r['avg_cost_per_case'])/3 + 0.25*float(r['avg_tat_days'])*3 + 0.25*float(r['backlog'])/3 + 0.20*float(r['rework_pct'])*5
        r['pain_index'] = round(pain,1)
        rows.append(r)
rows.sort(key=lambda x: x['pain_index'], reverse=True)
md=['# Cost-to-Serve Diagnostic','','| Unit | Pain Index | Main issue | Intervention |','|---|---:|---|---|']
for r in rows:
    issue = 'High cost + high backlog' if float(r['avg_cost_per_case'])>240 and float(r['backlog'])>200 else 'Medium operations pressure'
    action = 'Standardize workflow, automate first-touch checks, reduce rework' if issue.startswith('High') else 'Monitor and copy best practices'
    md.append(f"| {r['unit']} | {r['pain_index']} | {issue} | {action} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
