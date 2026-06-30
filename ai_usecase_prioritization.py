import csv
from pathlib import Path
DATA = Path(__file__).resolve().parents[1] / 'data' / 'workflow_ai_prioritization.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'ai_usecase_priority_matrix.md'
OUT.parent.mkdir(exist_ok=True)
rows=[]
with DATA.open() as f:
    for r in csv.DictReader(f):
        value = 0.30*float(r['volume'])/35 + 0.25*float(r['manual_effort_hours'])/6 + 0.20*float(r['error_rate_pct'])*5 + 0.25*float(r['citizen_impact'])
        feasibility = 0.60*float(r['automation_potential']) + 0.40*(100-float(r['implementation_complexity']))
        priority = 0.60*value + 0.40*feasibility
        r['priority_score'] = round(priority,1)
        r['decision'] = 'Wave 1' if priority >= 75 else 'Wave 2' if priority >= 60 else 'Later'
        rows.append(r)
rows.sort(key=lambda x: x['priority_score'], reverse=True)
md=['# AI Use-Case Prioritization Matrix','','| Process | Priority Score | Implementation Wave | Suggested AI use case |','|---|---:|---|---|']
for r in rows:
    usecase = 'LLM triage and workflow routing' if r['process']=='grievance triage' else 'OCR + rule validation' if r['process']=='document verification' else 'Automated SMS/WhatsApp status bot' if r['process']=='status communication' else 'Escalation prediction model'
    md.append(f"| {r['process']} | {r['priority_score']} | {r['decision']} | {usecase} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
