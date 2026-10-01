import json,time,urllib.request,urllib.parse
B='https://arctic-shift.photon-reddit.com/api/'
def get(ep,**p):
    url=B+ep+'?'+urllib.parse.urlencode(p)
    for i in range(3):
        try:
            d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'bbm-research/1.0'}),timeout=90))
            if d.get('data') is not None: return d['data']
        except Exception as e: pass
        time.sleep(4)
    return []
subs=['IndianSkincareAddicts','india','AskIndia','IndianMakeupAddicts','TwoXIndia','IndianMaleGrooming','bangalore','delhi','mumbai','IndiaSpeaks','indianbeautytalks','Dentistry_India','IndianTeenagers','IndiaTech']
terms=['teeth','whitening','perfora']
wins=[('2023-01-01','2024-06-01'),('2024-06-01','2025-06-01'),('2025-06-01','2026-10-01')]
posts={}
for s in subs:
  for t in terms:
    for a,b in wins:
      for x in get('posts/search',subreddit=s,title=t,after=a,before=b,limit=100,fields='id,title,selftext,num_comments,score,subreddit,created_utc'):
        posts[x['id']]=x
      time.sleep(1.2)
  print(s,len(posts),flush=True)
json.dump(posts,open('reddit_posts.json','w',encoding='utf-8'))
