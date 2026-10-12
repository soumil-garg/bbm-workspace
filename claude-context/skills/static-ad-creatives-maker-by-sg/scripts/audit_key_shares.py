"""For one audit folder: the share of audit texts the 3-labeller key marks positive per theme, with Wilson 95% intervals (n = audit size),
plus up to 3 key-positive texts per theme (cut to 15 words). Use it to quote uncleared or untested themes honestly: 'k of 100 random on-topic texts (95% interval a to b)'."""
import sys, os, json, re, io
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme_counter as T
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D = sys.argv[1].rstrip('/\\') + '/'
themes = json.load(open(D + 'themes.json', encoding='utf-8'))
texts = {x['id']: x['text'] for x in json.load(open(D + 'audit_reviews.json', encoding='utf-8'))}
labs = [{x['id']: set(x['yes']) for x in json.load(open(D + fn, encoding='utf-8'))['labels']} for fn in ('labels_claude_sub.json', 'labels_mini.json', 'labels_claude_main.json')]
N = len(texts)


def cut(t, n=15):
    w = re.sub(r'\s+', ' ', t.split('||')[-1]).strip().split(' ')
    return ' '.join(w[:n]) + (' ...' if len(w) > n else '')


rows = []
for t in themes:
    pos = [i for i in range(N) if sum(1 for L in labs if t in L[i]) >= 2]
    lo, hi = T.wilson(len(pos), N)
    rows.append((len(pos), t, lo, hi, pos))
for k, t, lo, hi, pos in sorted(rows, reverse=True):
    print('%-38s %3d of %d = %4.1f%% (95%% %.0f to %.0f)' % (t, k, N, 100.0 * k / N, 100 * lo, 100 * hi))
    for i in pos[:3]:
        print('      "%s"' % cut(texts[i]))
