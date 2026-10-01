import json,time,urllib.request,urllib.parse,re
B='https://arctic-shift.photon-reddit.com/api/'
def get(ep,**p):
    url=B+ep+'?'+urllib.parse.urlencode(p)
    for i in range(3):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'bbm-research/1.0'}),timeout=90))
            if d.get('data') is not None: return d['data']
        except Exception: pass
        time.sleep(4)
    return []
P=json.load(open('reddit_posts.json',encoding='utf-8'))
kw=re.compile(r'teeth|tooth|whiten|yellow|stain|smile|dent|perfora|charcoal|enamel',re.I)
rel=[p for p in P.values() if kw.search(p['title']+' '+(p.get('selftext') or ''))]
rel.sort(key=lambda p:-(p.get('num_comments') or 0))
print('relevant posts',len(rel))
out=[]
for p in rel[:45]:
    cs=get('comments/search',link_id=p['id'],limit=100,fields='body,score')
    cs=sorted([c for c in cs if c.get('body') and c['body'] not in('[deleted]','[removed]')],key=lambda c:-(c.get('score') or 0))
    out.append({'sub':p['subreddit'],'title':p['title'],'text':(p.get('selftext') or '')[:600],'n':p.get('num_comments'),'score':p.get('score'),'comments':[(c.get('score'),c['body'][:350]) for c in cs[:15]]})
    time.sleep(1.2)
json.dump(out,open('reddit_threads.json','w',encoding='utf-8'),ensure_ascii=False)
with open('reddit.txt','w',encoding='utf-8') as f:
    for t in out:
        f.write(f"\n##### r/{t['sub']} | {t['title']} | {t['n']} comments\n{t['text']}\n")
        for s,b in t['comments']: f.write(f"  [{s}] {b.replace(chr(10),' ')}\n")
print('done')
