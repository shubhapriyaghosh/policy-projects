import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data' / 'constituency_sample.csv'
OUT = Path(__file__).resolve().parents[1] / 'outputs' / 'constituency_priority_scorecard.md'
OUT.parent.mkdir(exist_ok=True)

def swing_score(margin):
    return max(0, 100 - margin * 8)

rows = []
with DATA.open() as f:
    for r in csv.DictReader(f):
        score = (
            0.15*float(r['youth_unemployment']) +
            0.14*float(r['water_issue']) +
            0.11*float(r['road_issue']) +
            0.18*float(r['anti_incumbency']) +
            0.14*(100-float(r['candidate_acceptance'])) +
            0.12*float(r['social_media_negative']) +
            0.10*swing_score(float(r['past_margin_pct'])) +
            0.06*(100-float(r['booth_worker_strength']))
        )
        r['priority_score'] = round(score, 1)
        if score >= 70: r['priority_band'] = 'High'
        elif score >= 55: r['priority_band'] = 'Medium'
        else: r['priority_band'] = 'Low'
        rows.append(r)
rows.sort(key=lambda x: x['priority_score'], reverse=True)

md = ['# Constituency Priority Scorecard', '', '| Rank | Ward | Score | Priority | Main action |', '|---:|---|---:|---|---|']
for i, r in enumerate(rows, 1):
    action = 'Immediate field visit + issue-specific message' if r['priority_band']=='High' else 'Monitor + targeted outreach' if r['priority_band']=='Medium' else 'Maintain presence'
    md.append(f"| {i} | {r['ward']} | {r['priority_score']} | {r['priority_band']} | {action} |")
OUT.write_text('\n'.join(md), encoding='utf-8')
print(f'Wrote {OUT}')
