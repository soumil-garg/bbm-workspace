"""Make the blind-audit folder for one text pool, replicating theme_counter's own sample (same loader, same seed), so the three labellers can start while the counter runs.

  python audit_make.py POOL.json THEMES.json OUTDIR [seed=11] [subset_ids.json]

Writes OUTDIR/audit_reviews.json (id, text), manifest.json (audit id -> source_id, product, stars) and themes.json (the binding question texts).
If subset_ids.json (a list of row ids in theme_counter's load order) is given, the 100 texts are drawn from that subset only: use it for pools where most texts are
off-topic (Reddit): draw from the texts the counter's relevance question says are on topic, so the audit has enough positives per theme.
Then: audit_label_mini.py (gpt-5-mini), a fresh Claude sub-agent, and Claude main label the 100 texts blind (no model output visible), and audit_score.py scores the counter.
"""
import sys, os, json, random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme_counter as T

pool, themes, out = sys.argv[1], sys.argv[2], sys.argv[3]
seed = int(sys.argv[4]) if len(sys.argv) > 4 else 11
subset = json.load(open(sys.argv[5], encoding='utf-8')) if len(sys.argv) > 5 else None
rows = T.load_rows(pool)
N = len(rows)
random.seed(seed)
pick = random.sample(range(N), min(100, N)) if subset is None else random.sample(subset, min(100, len(subset)))
os.makedirs(out, exist_ok=True)
json.dump([{'id': k, 'text': rows[i]['text']} for k, i in enumerate(pick)], open(out + '/audit_reviews.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump([{'id': k, 'source_id': rows[i]['id'], 'product': rows[i]['product'], 'stars': rows[i]['stars']} for k, i in enumerate(pick)], open(out + '/manifest.json', 'w', encoding='utf-8'), indent=1)
json.dump(json.load(open(themes, encoding='utf-8')), open(out + '/themes.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('rows', N, '| audit sample', len(pick), '| written to', out)
