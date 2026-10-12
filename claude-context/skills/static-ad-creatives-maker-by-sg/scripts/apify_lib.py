"""Small Apify helper used by reddit_pull.py, amazon_pull.py and google_pull.py (proven on Daigo, 2026-10-09).

Token: user env var APIFY_TOKEN (falls back to the Windows user registry). It is never printed.
Every run is started with maxTotalChargeUsd, so one run cannot spend more than its cap.
Pay-per-event actors bill by item; the cost on the run object lags by about a minute after the run ends, so budget with
(items x list price) and read the account total with month_usage(), never trust usageTotalUsd the moment a run finishes.
"""
import os, sys, io, json, time, urllib.request, urllib.error, urllib.parse

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
except Exception:
    pass


def _token():
    t = os.environ.get('APIFY_TOKEN')
    if t:
        return t
    import winreg
    k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment')
    return winreg.QueryValueEx(k, 'APIFY_TOKEN')[0]


_TOK = None


def tok():
    global _TOK
    if _TOK is None:
        _TOK = _token()
    return _TOK


def _req(method, path, body=None, params=None, timeout=90):
    q = {'token': tok()}
    if params:
        q.update(params)
    url = 'https://api.apify.com/v2/' + path + '?' + urllib.parse.urlencode(q)
    data = json.dumps(body).encode('utf-8') if body is not None else None
    headers = {'User-Agent': 'Mozilla/5.0'}
    if data is not None:
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        return {'error': 'HTTP %s %s' % (e.code, e.read().decode('utf-8', 'replace')[:400].replace(tok(), 'TOKEN'))}
    except Exception as e:
        return {'error': repr(e)[:240].replace(tok(), 'TOKEN')}


def start(actor, inp, cap_usd, timeout_secs=900, memory_mbytes=None):
    params = {'maxTotalChargeUsd': cap_usd, 'timeout': timeout_secs}
    if memory_mbytes:
        params['memory'] = memory_mbytes
    return _req('POST', 'acts/%s/runs' % actor, body=inp, params=params)


def wait(run_id, max_wait=900, poll=6):
    t0 = time.time()
    last = {}
    while time.time() - t0 < max_wait:
        r = _req('GET', 'actor-runs/' + run_id)
        d = r.get('data') or {}
        last = d or r
        if d.get('status') in ('SUCCEEDED', 'FAILED', 'ABORTED', 'TIMED-OUT'):
            return d
        time.sleep(poll)
    _req('POST', 'actor-runs/%s/abort' % run_id)
    return {'status': 'WAIT-EXPIRED-ABORTED', 'id': run_id, 'last': last}


def dataset_items(dataset_id, max_items=100000):
    out = []
    off = 0
    while off < max_items:
        r = _req('GET', 'datasets/%s/items' % dataset_id, params={'format': 'json', 'clean': 'true', 'offset': off, 'limit': 1000}, timeout=180)
        if isinstance(r, dict) and 'error' in r:
            return out, r['error']
        if not r:
            break
        out.extend(r)
        if len(r) < 1000:
            break
        off += 1000
    return out, None


def run_and_collect(tag, actor, inp, cap_usd, max_wait=900, timeout_secs=900):
    """start, wait, fetch the dataset; returns a dict with status, items, secs (cost fields lag, see module doc)"""
    t0 = time.time()
    s = start(actor, inp, cap_usd, timeout_secs=timeout_secs)
    if 'error' in s:
        return {'tag': tag, 'ok': False, 'status': 'START-FAILED', 'err': s['error'], 'secs': round(time.time() - t0, 1), 'cost': 0.0, 'items': []}
    run = s['data']
    d = wait(run['id'], max_wait=max_wait)
    items, err = [], None
    if d.get('defaultDatasetId'):
        items, err = dataset_items(d['defaultDatasetId'])
    return {'tag': tag, 'ok': d.get('status') == 'SUCCEEDED', 'status': d.get('status'), 'run_id': run['id'], 'dataset': d.get('defaultDatasetId'),
            'cost': d.get('usageTotalUsd') or 0.0, 'secs': round(time.time() - t0, 1), 'items': items, 'err': err, 'statusMessage': d.get('statusMessage')}


def month_usage():
    """(usage so far this billing cycle in USD, the account's monthly usage limit). Read-only, free."""
    r = _req('GET', 'users/me/limits')
    d = r.get('data') or {}
    return (d.get('current') or {}).get('monthlyUsageUsd'), (d.get('limits') or {}).get('maxMonthlyUsageUsd')


def cycle():
    r = _req('GET', 'users/me/limits')
    return (r.get('data') or {}).get('monthlyUsageCycle')
