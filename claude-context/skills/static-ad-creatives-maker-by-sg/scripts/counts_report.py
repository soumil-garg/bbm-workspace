"""Turn theme_counter output plus the blind-audit verdicts into the counted-pains tables for the vault note (Stage 2 section 3 / Stage 3b).

  python counts_report.py --pool pool.json --counter-out OUT --audit-results AUDIT/audit_results.json --title "Amazon.in reviews" [--base-theme on_topic_drink] [--quotes 2] [--out report.md]

- Counts are Jev answers at probability >= 0.5, shares carry Wilson 95% intervals, and the 'Range' column shows the yes count if every flagged answer (Jev 0.25 to 0.75,
  models disagree, Luna refused) went one way or the other.
- With --base-theme (Reddit): shares are taken among the texts the base theme calls on topic, not among all texts.
- Only CLEARED themes (audit: >= 5 key positives, precision >= 0.75, share error within 5 points) go in the main table. The rest are listed as raw counts marked do-not-quote.
- Sample quotes are verbatim, cut to 15 words, highest Jev probability first.
"""
import sys, os, json, argparse, io, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import theme_counter as T

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass


def cut(text, n=15):
    w = re.sub(r'\s+', ' ', text).strip().split(' ')
    return ' '.join(w[:n]) + (' ...' if len(w) > n else '')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pool', required=True)
    ap.add_argument('--counter-out', required=True)
    ap.add_argument('--audit-results', required=True)
    ap.add_argument('--title', required=True)
    ap.add_argument('--base-theme', default='')
    ap.add_argument('--quotes', type=int, default=2)
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    rows = T.load_rows(a.pool)
    ans = {x['id']: x for x in json.load(open(a.counter_out.rstrip('/\\') + '/theme_answers.json', encoding='utf-8'))}
    aud = json.load(open(a.audit_results, encoding='utf-8'))
    themes = list(next(iter(ans.values()))['answers'].keys())
    S = [r['id'] for r in rows]
    if a.base_theme:
        S = [i for i in S if (ans[i]['answers'][a.base_theme]['jev'] or 0) >= 0.5]
    Sset = set(S)
    crit = [i for i in S if 1 <= rows[i]['stars'] <= 3]
    byid = {r['id']: r for r in rows}
    lines = ['### %s: counted themes' % a.title, '',
             'Texts counted: %d%s%s. Counter: Jev (counts) with Luna as second reader; audit verdicts from %s.' % (
                 len(S), (' of %d (the base question "%s" says on topic)' % (len(rows), a.base_theme)) if a.base_theme else '',
                 ('; rated 1 to 3 stars: %d' % len(crit)) if crit else '', os.path.basename(os.path.dirname(a.audit_results.rstrip('/\\')) + '/' + os.path.basename(a.audit_results))), '']
    out_main, out_rest = [], []
    for t in themes:
        if t == a.base_theme:
            continue
        yes = [i for i in S if (ans[i]['answers'][t]['jev'] or 0) >= 0.5]
        flagged = []
        for i in S:
            jp = ans[i]['answers'][t]['jev']
            lp = ans[i]['answers'][t]['luna']
            reason = None
            if 0.25 <= jp <= 0.75:
                reason = 'mid'
            elif lp is None:
                reason = 'refused' if any(ans[i]['answers'][x]['luna'] is not None for x in themes) or True else None
            elif (lp >= 0.5) != (jp >= 0.5):
                reason = 'disagree'
            if reason:
                flagged.append((i, jp >= 0.5))
        fy = sum(1 for _, y in flagged if y)
        fn = len(flagged) - fy
        lo, hi = T.wilson(len(yes), len(S))
        yc = [i for i in yes if i in set(crit)]
        clo, chi = T.wilson(len(yc), len(crit)) if crit else (0, 0)
        v = (aud['themes'].get(t) or {}).get('verdict', '?')
        rec = {'t': t, 'yes': len(yes), 'share': 100.0 * len(yes) / max(1, len(S)), 'lo': 100 * lo, 'hi': 100 * hi, 'yc': len(yc), 'sc': (100.0 * len(yc) / len(crit)) if crit else None,
               'clo': 100 * clo, 'chi': 100 * chi, 'rng': '%d-%d' % (len(yes) - fy, len(yes) + fn), 'flag': len(flagged), 'verdict': v}
        top = sorted(yes, key=lambda i: -ans[i]['answers'][t]['jev'])[:a.quotes]
        rec['quotes'] = [cut(byid[i]['text']) for i in top]
        (out_main if v == 'CLEARED' else out_rest).append(rec)
    hdr = '| Theme | Yes | Share (95% interval) | ' + ('Yes in 1 to 3 star | Share of critical (95%) | ' if crit else '') + 'Range if flagged resolved | Flagged |'
    lines += ['**Cleared by the audit (safe to quote):**', '', hdr, '|---|---|---|' + ('---|---|' if crit else '') + '---|---|']
    for r in sorted(out_main, key=lambda r: -r['share']):
        lines.append('| %s | %d | %.1f%% (%.0f to %.0f) | ' % (r['t'], r['yes'], r['share'], r['lo'], r['hi']) + ('%d | %.1f%% (%.0f to %.0f) | ' % (r['yc'], r['sc'], r['clo'], r['chi']) if crit else '') + '%s | %d |' % (r['rng'], r['flag']))
    lines += ['', '**Not cleared or untested (raw Jev counts, do not quote a share):**', '', '| Theme | Yes | Audit verdict |', '|---|---|---|']
    for r in sorted(out_rest, key=lambda r: -r['yes']):
        lines.append('| %s | %d | %s |' % (r['t'], r['yes'], r['verdict']))
    lines += ['', '**Verbatim samples (highest Jev probability, cut to 15 words) for cleared themes:**', '']
    for r in sorted(out_main, key=lambda r: -r['share']):
        for q in r['quotes']:
            lines.append('- %s: "%s"' % (r['t'], q))
    txt = '\n'.join(lines) + '\n'
    if a.out:
        open(a.out, 'w', encoding='utf-8').write(txt)
    print(txt)


if __name__ == '__main__':
    main()
