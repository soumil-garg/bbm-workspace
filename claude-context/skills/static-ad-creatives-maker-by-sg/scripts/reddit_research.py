"""Reddit research through the Arctic Shift public archive (Reddit blocks direct access).

Usage:
  python reddit_research.py --out C:\\cca\\brand\\research --subs IndianSkincareAddicts,india --terms teeth,whitening --from 2023-01-01 --top 45
Optional: --kw "teeth|tooth|whiten"   regex to keep only relevant posts (default: the terms)
Writes: reddit_posts.json, reddit_threads.json, reddit.txt (human-readable, top comments by score).
Notes: title search times out without a date window, so it runs yearly windows. Sleep ~1.2s between calls.
"""
import argparse, json, os, re, time, urllib.parse, urllib.request
from datetime import date

B = 'https://arctic-shift.photon-reddit.com/api/'


def get(ep, **p):
    url = B + ep + '?' + urllib.parse.urlencode(p)
    for _ in range(3):
        try:
            d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'bbm-research/1.0'}), timeout=90))
            if d.get('data') is not None:
                return d['data']
        except Exception:
            pass
        time.sleep(4)
    return []


def windows(start):
    y0 = int(start[:4]); y1 = date.today().year
    out = []
    for y in range(y0, y1 + 1):
        a = start if y == y0 else f'{y}-01-01'
        out.append((a, f'{y + 1}-01-01'))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--subs', required=True)
    ap.add_argument('--terms', required=True)
    ap.add_argument('--from', dest='start', default='2023-01-01')
    ap.add_argument('--top', type=int, default=45)
    ap.add_argument('--kw', default=None)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    subs = [s.strip() for s in a.subs.split(',') if s.strip()]
    terms = [t.strip() for t in a.terms.split(',') if t.strip()]
    kw = re.compile(a.kw or '|'.join(map(re.escape, terms)), re.I)
    posts = {}
    for s in subs:
        for t in terms:
            for lo, hi in windows(a.start):
                for x in get('posts/search', subreddit=s, title=t, after=lo, before=hi, limit=100,
                             fields='id,title,selftext,num_comments,score,subreddit,created_utc'):
                    posts[x['id']] = x
                time.sleep(1.2)
        print(s, len(posts), flush=True)
    json.dump(posts, open(os.path.join(a.out, 'reddit_posts.json'), 'w', encoding='utf-8'))
    rel = [p for p in posts.values() if kw.search(p['title'] + ' ' + (p.get('selftext') or ''))]
    rel.sort(key=lambda p: -(p.get('num_comments') or 0))
    print('relevant', len(rel), flush=True)
    out = []
    for p in rel[:a.top]:
        cs = get('comments/search', link_id=p['id'], limit=100, fields='body,score')
        cs = sorted([c for c in cs if c.get('body') and c['body'] not in ('[deleted]', '[removed]')], key=lambda c: -(c.get('score') or 0))
        out.append({'sub': p['subreddit'], 'title': p['title'], 'text': (p.get('selftext') or '')[:600], 'n': p.get('num_comments'),
                    'comments': [(c.get('score'), c['body'][:350]) for c in cs[:15]]})
        time.sleep(1.2)
    json.dump(out, open(os.path.join(a.out, 'reddit_threads.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    with open(os.path.join(a.out, 'reddit.txt'), 'w', encoding='utf-8') as f:
        for t in out:
            f.write(f"\n##### r/{t['sub']} | {t['title']} | {t['n']} comments\n{t['text']}\n")
            for s_, b in t['comments']:
                f.write(f"  [{s_}] {b.replace(chr(10), ' ')}\n")
    print('done')


if __name__ == '__main__':
    main()
