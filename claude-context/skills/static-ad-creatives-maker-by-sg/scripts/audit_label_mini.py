"""Blind audit labeller #2: gpt-5-mini answers the same yes/no theme questions on the audit texts (text only: no stars, no product, no model output).
Part of the 100-text blind audit in references/theme-question-rules.md (three labellers: a fresh Claude agent, gpt-5-mini, Claude main; key = majority of 3).

  python audit_label_mini.py --audit AUDIT_DIR/audit_reviews.json --themes AUDIT_DIR/themes.json --out AUDIT_DIR/labels_mini.json --about "customer reviews of chaas and buttermilk premixes written by Indian shoppers on Amazon.in"

Output format (same as the other labellers): {"labeler": "gpt-5-mini", "labels": [{"id": 0, "yes": ["theme", ...], "language": "english"}, ...]}
OPENAI_API_KEY comes from the user environment, never printed. Cost guard: reasoning_effort low, 100 calls, about $0.10 to $0.20. Prices are assumed ($0.25 in / $2.00 out per M).
"""
import sys, os, json, time, io, argparse
from concurrent.futures import ThreadPoolExecutor
import urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme_counter import getenv

MODEL = 'gpt-5-mini'
LANGS = ['english', 'hinglish', 'hindi', 'other']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audit', required=True)
    ap.add_argument('--themes', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--about', required=True, help='one line: what the texts are (source, product type, who wrote them)')
    a = ap.parse_args()
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass
    reviews = json.load(open(a.audit, encoding='utf-8'))
    themes = json.load(open(a.themes, encoding='utf-8'))
    key = getenv('OPENAI_API_KEY')
    if not key:
        sys.exit('OPENAI_API_KEY not set')
    hdr = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}
    rules = ('You label texts: %s.\nFor the text you are given, answer each of the %d questions with true or false, judging ONLY from what the text says.\n'
             'Rules:\n0. Answer exactly the question as worded, including any \'Answer no if ...\' sentence: it is binding.\n'
             '1. Answer true only if the text itself says it or clearly implies it. If the text does not mention the thing, answer false.\n'
             '2. Read each question literally, including negation. "It did not taste good" is NOT a good-taste statement. "Not expensive" is NOT a price complaint.\n'
             '3. Texts may be in English, Hinglish (Hindi written in Roman letters) or Hindi. Understand them as a native Indian reader would.\n'
             '4. Do not use outside knowledge. Several questions can be true at once. Most questions will be false for most texts.\n'
             'Also give the language of the text: english, hinglish, hindi or other.') % (a.about, len(themes))
    questions = '\n'.join('- %s: %s' % (k, v) for k, v in themes.items())
    schema = {'type': 'object', 'properties': {**{k: {'type': 'boolean'} for k in themes}, 'language': {'type': 'string', 'enum': LANGS}},
              'required': list(themes) + ['language'], 'additionalProperties': False}

    def call(r):
        body = json.dumps({'model': MODEL, 'messages': [{'role': 'system', 'content': rules + '\n\nQuestions:\n' + questions}, {'role': 'user', 'content': 'Text:\n' + r['text']}],
                           'response_format': {'type': 'json_schema', 'json_schema': {'name': 'labels', 'strict': True, 'schema': schema}},
                           'reasoning_effort': 'low', 'max_completion_tokens': 4000}).encode('utf-8')
        last = None
        for t in range(6):
            req = urllib.request.Request('https://api.openai.com/v1/chat/completions', data=body, headers=hdr, method='POST')
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    d = json.loads(resp.read().decode('utf-8'))
                out = json.loads(d['choices'][0]['message']['content'])
                u = d.get('usage', {})
                return {'id': r['id'], 'yes': [k for k in themes if out.get(k)], 'language': out.get('language'), '_in': u.get('prompt_tokens', 0), '_out': u.get('completion_tokens', 0)}
            except urllib.error.HTTPError as e:
                detail = e.read().decode('utf-8', 'ignore')[:300]
                if e.code in (408, 409, 429) or e.code >= 500:
                    time.sleep(2 ** t)
                    last = 'HTTP %s %s' % (e.code, detail)
                    continue
                raise RuntimeError('HTTP %s %s' % (e.code, detail))
            except Exception as e:
                time.sleep(2 ** t)
                last = str(e)
        raise RuntimeError('gave up: ' + str(last))

    t0 = time.time()
    with ThreadPoolExecutor(4) as ex:
        res = list(ex.map(call, reviews))
    tin, tout = sum(x['_in'] for x in res), sum(x['_out'] for x in res)
    usd = tin * 0.25 / 1e6 + tout * 2.0 / 1e6
    ledger = 'C:/cca/_ledger/openai_chat_usage.jsonl'
    os.makedirs(os.path.dirname(ledger), exist_ok=True)
    with open(ledger, 'a', encoding='utf-8') as f:
        f.write(json.dumps({'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'tag': 'audit_label_mini', 'model': MODEL, 'calls': len(res), 'input_tokens': tin, 'output_tokens': tout, 'usd_assumed_prices': round(usd, 4)}) + '\n')
    json.dump({'labeler': MODEL, 'labels': [{k: v for k, v in x.items() if not k.startswith('_')} for x in res]}, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%d texts labelled by %s in %.0fs; tokens in %d, out %d; cost about $%.3f (assumed prices)' % (len(res), MODEL, time.time() - t0, tin, tout, usd))
    print('positives per theme:', {k: sum(1 for x in res if k in x['yes']) for k in themes})


if __name__ == '__main__':
    main()
