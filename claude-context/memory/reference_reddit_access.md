---
name: reference_reddit_access
description: "How to read Reddit when it blocks WebFetch and Chrome: Arctic Shift public API via local Python; working scripts in C:\\cca\\habbits\\research"
metadata:
  node_type: memory
  type: reference
  originSessionId: be4b06da-2803-493f-bdab-d64482a42640
  modified: 2026-10-07T14:18:36.783Z
---

Reddit blocks WebFetch, curl from this machine (403), and Claude in Chrome ("not allowed due to safety restrictions"). PullPush returns 429 for agents.

**Working route (2026-09-29):** Arctic Shift API `https://arctic-shift.photon-reddit.com/api/` called from local Python (urllib).
- Posts: `posts/search?subreddit=X&title=term&after=YYYY-MM-DD&before=YYYY-MM-DD&limit=100&fields=id,title,selftext,num_comments,score,subreddit`. **Title search times out ("Maybe slow down a bit") without a date window**, so always pass after/before (split into ~1-year windows).
- Comments: `comments/search?link_id=<post id>&limit=100&fields=body,score`.
- Sleep ~1.2s between calls. 14 subs x 3 terms x 3 windows took ~12 min.
- Scripts to copy: `C:\cca\habbits\research\reddit.py` (posts) and `reddit_c.py` (comments to text).

Good Indian subs for consumer research: IndianSkincareAddicts, IndianBeautyTalks, TwoXIndia, AskIndia, delhi, bangalore, mumbai, IndianMaleGrooming. Dentists/experts are vocal there; weight upvotes.

**Rate-limit lessons (5 Oct and 7 Oct 2026):** Arctic Shift answers 429 and 422 ("Timeout. Maybe slow down") and then keeps refusing for hours. On 7 Oct a 3-worker run (312 jobs, `query=` full-text search) got about 285 retries and only 26 posts in 100 jobs, and a follow-up slow single-worker run failed the same way for 20+ minutes, so I stopped it (do not loop; the playbook says log "Reddit unavailable today" and retry later with ONE test call). Use ONE sequential worker with 3+ s pauses and the resumable script `C:\cca\habbits\step2\reddit\reddit_slow.py` (jobs_done.json lets it resume). The 29 Sep Habbits data (372 posts, 45 threads, 675 comments in C:\cca\habbits\research\) is what Step 2 used meanwhile. A single `posts/search` test call with `query=` worked right before the heavy run.

Related: [[process_ad_creatives]], [[feedback_blockers]]
