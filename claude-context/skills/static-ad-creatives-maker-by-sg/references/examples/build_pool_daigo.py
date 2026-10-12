"""Build the Daigo text pools for theme counting (Stage 2). Public text only; names, handles, emails and URLs are stripped later by theme_counter.strip_pii,
and no username is written into the pools. Three pools, because the sources behave differently:
  pool_amazon.json   list of {product, stars, text}  (Amazon.in reviews; stars drive the 1-3 star share)
  pool_reddit.json   list of {product, stars:0, text} (Reddit comments and the posts themselves, tagged by tier)
  pool_forums.json   list of {product, stars:0, text} (open-forum texts from the forum agent)
Each text also gets an id map in pool_meta.json so any count can be traced back to source, date and thread."""
import json, re, os, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
R = 'C:/cca/daigo/research/'
OUT = R + 'count/'
os.makedirs(OUT, exist_ok=True)
html_ent = re.compile(r'&(amp|lt|gt|quot|#x200B|#39);')


def clean(t):
    t = (t or '').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#x200B;', ' ').replace('&#39;', "'")
    t = re.sub(r'\s+', ' ', t).strip()
    return t


# Amazon
am = json.load(open(R + 'amazon/amazon_reviews_all.json', encoding='utf-8'))
amz = []
meta = {'amazon': [], 'reddit': [], 'forums': []}
for r in am:
    text = clean((r.get('title') or '') + '. ' + (r.get('text') or ''))
    if len(text) < 12:
        continue
    st = int(r['rating']) if r.get('rating') else 0
    amz.append({'product': '%s | %s' % (r.get('group'), r.get('brand')), 'stars': st, 'text': text})
    meta['amazon'].append({'asin': r['asin'], 'review_id': r['review_id'], 'group': r.get('group'), 'brand': r.get('brand'), 'date': r.get('date'), 'stars': st})
json.dump(amz, open(OUT + 'pool_amazon.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('amazon texts:', len(amz), '| 1-3 star:', sum(1 for x in amz if 0 < x['stars'] <= 3))

# Reddit: comments (phase 2, top-up) + the posts of selected threads
D = R + 'reddit_apify/data/'
posts = {p['id']: p for p in json.load(open(D + 'p1_posts_all.json', encoding='utf-8'))}
for p in json.load(open(D + 'p1b_posts_all.json', encoding='utf-8')):
    posts.setdefault(p['id'], p)
sel = {}
for fn in ['p2_selection.json', 'p2b_selection.json']:
    if os.path.exists(D + fn):
        for s in json.load(open(D + fn, encoding='utf-8')):
            sel[s['id']] = s
red = []
seen = set()
nthreads = collections.Counter()
for fn in ['p2_comments_all.json', 'p2b_comments_all.json']:
    for c in json.load(open(D + fn, encoding='utf-8')):
        cid = c.get('id')
        if not cid or cid in seen:
            continue
        seen.add(cid)
        body = clean(c.get('body'))
        if body in ('[deleted]', '[removed]') or len(body) < 25:
            continue
        pid = (c.get('postId') or '').replace('t3_', '')
        tier = (sel.get(pid) or {}).get('tier', 'T1b')
        title = clean(c.get('postTitle') or (posts.get(pid) or {}).get('title') or '')
        red.append({'product': 'reddit_comment | %s' % tier, 'stars': 0, 'text': (title + ' || ' + body) if title else body})
        meta['reddit'].append({'kind': 'comment', 'id': cid, 'post_id': pid, 'sub': (posts.get(pid) or {}).get('subreddit'), 'date': c.get('createdAt'), 'score': c.get('score'), 'tier': tier})
        nthreads[pid] += 1
for pid, s in sel.items():
    p = posts.get(pid) or {}
    body = clean(((p.get('title') or '') + '. ' + (p.get('body') or '')))
    if len(body) >= 25:
        red.append({'product': 'reddit_post | %s' % s.get('tier', 'T1b'), 'stars': 0, 'text': body})
        meta['reddit'].append({'kind': 'post', 'id': pid, 'post_id': pid, 'sub': p.get('subreddit'), 'date': p.get('created_utc'), 'score': p.get('score'), 'tier': s.get('tier')})
# the comment-level brand mentions (harshmaur)
for c in json.load(open(D + 'p1_comment_mentions.json', encoding='utf-8')):
    body = clean(c.get('body'))
    if len(body) >= 25 and c.get('id') not in seen:
        seen.add(c.get('id'))
        red.append({'product': 'reddit_comment | mention', 'stars': 0, 'text': body})
        meta['reddit'].append({'kind': 'comment', 'id': c.get('id'), 'post_id': c.get('parsedPostId'), 'sub': c.get('subredditName'), 'date': c.get('commentCreatedAt'), 'score': c.get('score'), 'tier': 'mention'})
json.dump(red, open(OUT + 'pool_reddit.json', 'w', encoding='utf-8'), ensure_ascii=False)
# core pool for counting: T1/T1b/T3 threads in full; T2 and mention comments only when the comment itself names the drink (or a brand), baking threads dropped
FOOD = re.compile(r'\b(chaas|chaach|chhaas|chach|mattha|majjige|butter ?milk|lassi|jal ?jeera|jaljira|dahi|curd)\b', re.I)
BRAND = re.compile(r'\b(amul|mille|pod nutrition|daigo)\b', re.I)
BAKING = re.compile(r'\b(flour|cake|pancake|biscuit|bisquick|ranch|dressing|baking|bake|dumpling|cornbread|waffle|fried chicken|muffin|scone)\b', re.I)
core = []
for x in red:
    kind = x['product']
    t = x['text']
    body = t.split('||', 1)[-1]
    if kind.endswith('| T1') or kind.endswith('| T1b') or kind.endswith('| T3'):
        core.append(x)
    elif kind.endswith('| T2') and FOOD.search(body) and not BAKING.search(t):
        core.append(x)
    elif kind.endswith('| mention') and (FOOD.search(t) or BRAND.search(t)) and not BAKING.search(t):
        core.append(x)
json.dump(core, open(OUT + 'pool_reddit_core.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('reddit core pool for counting:', len(core), dict(collections.Counter(x['product'] for x in core)))
print('reddit texts:', len(red), '| comments', sum(1 for x in red if x['product'].startswith('reddit_comment')), '| posts', sum(1 for x in red if x['product'].startswith('reddit_post')),
      '| threads with comments', len(nthreads))

# forums
fr = []
skipped = collections.Counter()
for fn in ['forum_texts.json', 'forum_texts_addendum.json']:
    p = R + 'reddit/' + fn
    if os.path.exists(p):
        d = json.load(open(p, encoding='utf-8'))
        rows = d if isinstance(d, list) else d.get('texts') or list(d.values())
        for r in rows:
            if isinstance(r, dict):
                t = clean(((r.get('title') or '') + '. ' + (r.get('body') or r.get('text') or r.get('snippet') or r.get('quote') or '')).strip('. '))
                src = r.get('source') or r.get('site') or r.get('src') or 'forum'
                if src in ('reddit', 'daigo_site_reviews', 'pod_site_reviews'):
                    skipped[src] += 1          # reddit snippets are covered by the Apify pull; brand-hosted reviews are curated, not independent
                    continue
                if len(t) >= 20:
                    fr.append({'product': 'forum | %s' % src, 'stars': 0, 'text': t})
                    meta['forums'].append({'source': src, 'url': r.get('url'), 'date': r.get('date')})
json.dump(fr, open(OUT + 'pool_forums.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('forum texts:', len(fr), '| by source:', dict(collections.Counter(x['product'] for x in fr).most_common(8)), '| skipped:', dict(skipped))
json.dump(meta, open(OUT + 'pool_meta.json', 'w', encoding='utf-8'), ensure_ascii=False)
