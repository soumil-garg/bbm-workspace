"""Generate or edit one image through the OpenAI API and log the cost.

Usage:
  python gen_image.py --prompt-file p.txt --out out.png [--ref ref1.jpg --ref ref2.png] [--model gpt-image-2.5-sunburst]
                      [--size 1024x1280|1024x1024|1024x1536|1536x1024] [--quality high] [--tag C1_M_OneTube]
  python gen_image.py --ledger          (print spend so far and the estimated balance)
  python gen_image.py --check           (one tiny gpt-5-mini call, about $0.00002: proves the key works and the account has credit; run it before a big round)
The key is the user environment variable OPENAI_API_KEY (read from the registry first). If it is missing or rejected, ask Soumil to run C:/cca/tools/set_openai_key.ps1 after copying the key; never ask him to paste a key into the chat.

Models (decided 2026-10-03): gpt-image-2.5-sunburst for finals, gpt-image-2.5-flare for fast drafts.
With one or more --ref it calls /v1/images/edits (real product photo attached); with none, /v1/images/generations.
Cost = text-in $5/M + image-in $8/M + image-out $30/M tokens (same for both 2.5 models), from the usage block in the response.
Ledger: C:/cca/_ledger/openai_images.jsonl and C:/cca/_ledger/balance.json ({"start_usd":16.0,"as_of":"2026-10-04"}).
The API key cannot read the real balance, so the estimate is start balance minus ledger spend since then. Update
balance.json whenever Soumil tops up or tells you the real figure. A warning prints below $3 estimated.
"""
import argparse, base64, json, os, sys, time, mimetypes
import requests

LEDGER_DIR = 'C:/cca/_ledger'
LEDGER = LEDGER_DIR + '/openai_images.jsonl'
BAL = LEDGER_DIR + '/balance.json'
WARN_BELOW = 3.0


def key():
    # The user environment variable in the registry is the source of truth (2026-10-10): a rotated key takes effect at once,
    # while os.environ is only a snapshot from when the parent app started and keeps the old key until that app restarts.
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as h:
            v = winreg.QueryValueEx(h, 'OPENAI_API_KEY')[0]
            if v:
                return v
    except Exception:
        pass
    return os.environ.get('OPENAI_API_KEY')


def cost_of(u):
    det = u.get('input_tokens_details') or {}
    img_in = det.get('image_tokens', 0)
    txt_in = det.get('text_tokens', max(u.get('input_tokens', 0) - img_in, 0))
    return txt_in * 5e-6 + img_in * 8e-6 + u.get('output_tokens', 0) * 30e-6


def ledger_status():
    os.makedirs(LEDGER_DIR, exist_ok=True)
    if not os.path.exists(BAL):
        json.dump({'start_usd': 16.0, 'as_of': '2026-10-04'}, open(BAL, 'w'))
    b = json.load(open(BAL))
    spent, n = 0.0, 0
    if os.path.exists(LEDGER):
        for line in open(LEDGER, encoding='utf-8'):
            r = json.loads(line)
            if r['ts'] >= b['as_of']:
                spent += r['usd']
                n += 1
    return b['start_usd'], spent, n


def check_key():
    k = key()
    if not k:
        sys.exit('ERROR: OPENAI_API_KEY is not set. Ask Soumil to copy the key and run C:/cca/tools/set_openai_key.ps1 (never ask him to paste the key into the chat).')
    r = requests.post('https://api.openai.com/v1/chat/completions', headers={'Authorization': 'Bearer ' + k, 'Content-Type': 'application/json'},
                      json={'model': 'gpt-5-mini', 'messages': [{'role': 'user', 'content': 'Reply with the single word ok.'}], 'reasoning_effort': 'minimal', 'max_completion_tokens': 64}, timeout=60)
    if r.status_code == 200:
        u = r.json().get('usage', {})
        print('KEY OK: the account answered (about $%.5f); key ends ...%s' % (u.get('prompt_tokens', 0) * 0.25e-6 + u.get('completion_tokens', 0) * 2e-6, k[-4:]))
    else:
        try:
            e = r.json().get('error', {})
        except Exception:
            e = {}
        print('KEY PROBLEM: HTTP %s %s %s' % (r.status_code, e.get('code'), (e.get('message') or r.text)[:160]))
        if r.status_code == 429:
            print('429 insufficient_quota or credit_balance_exhausted means no credit: tell Soumil which account needs the top-up (the account behind the key ending ...%s); topping up is his action.' % k[-4:])
        sys.exit(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--prompt-file')
    ap.add_argument('--out')
    ap.add_argument('--ref', action='append', default=[])
    ap.add_argument('--model', default='gpt-image-2.5-sunburst')
    ap.add_argument('--size', default='1024x1024')
    ap.add_argument('--quality', default='high')
    ap.add_argument('--tag', default='')
    ap.add_argument('--ledger', action='store_true')
    ap.add_argument('--check', action='store_true')
    a = ap.parse_args()
    start, spent, n = ledger_status()
    if a.check:
        check_key()
        return
    if a.ledger:
        print(f'start ${start:.2f}, logged spend ${spent:.2f} over {n} images, estimated balance ${start - spent:.2f}')
        return
    prompt = open(a.prompt_file, encoding='utf-8').read()
    k = key()
    if not k:
        sys.exit('ERROR: OPENAI_API_KEY is not set. Ask Soumil to copy the key and run C:/cca/tools/set_openai_key.ps1 (never ask him to paste the key into the chat).')
    hdr = {'Authorization': 'Bearer ' + k}
    t = time.time()
    if a.ref:
        files = [('image[]', (os.path.basename(p), open(p, 'rb'), mimetypes.guess_type(p)[0] or 'image/png')) for p in a.ref]
        r = requests.post('https://api.openai.com/v1/images/edits', headers=hdr,
                          data={'model': a.model, 'prompt': prompt, 'size': a.size, 'quality': a.quality, 'n': 1}, files=files, timeout=600)
    else:
        r = requests.post('https://api.openai.com/v1/images/generations', headers={**hdr, 'Content-Type': 'application/json'},
                          json={'model': a.model, 'prompt': prompt, 'size': a.size, 'quality': a.quality, 'n': 1}, timeout=600)
    if r.status_code != 200:
        print('ERROR', r.status_code, r.text[:500])
        sys.exit(1)
    d = r.json()
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, 'wb').write(base64.b64decode(d['data'][0]['b64_json']))
    usd = cost_of(d.get('usage') or {})
    with open(LEDGER, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'tag': a.tag or os.path.basename(a.out), 'model': a.model,
                            'size': a.size, 'usd': round(usd, 4), 'secs': round(time.time() - t)}) + '\n')
    est = start - spent - usd
    print(f'ok {a.out}  ${usd:.3f}  {round(time.time() - t)}s  est balance ${est:.2f}')
    if est < WARN_BELOW:
        print(f'WARNING: estimated OpenAI balance ${est:.2f} is below ${WARN_BELOW:.0f}. Tell Soumil before generating more.')


if __name__ == '__main__':
    main()
