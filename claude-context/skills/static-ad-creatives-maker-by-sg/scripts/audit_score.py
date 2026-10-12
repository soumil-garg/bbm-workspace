"""Blind-audit scorer for theme_counter.py (rules in references/theme-question-rules.md).
Key = majority of three blind labellers (labels_claude_sub.json, labels_mini.json, labels_claude_main.json in the audit folder).
A theme is CLEARED for counting when, on the audit sample, it has >= 5 key positives, precision >= 0.75 and |share error| <= 5 points.
Fewer than 5 key positives = UNTESTED (report it, do not quote a share). Models are scored at threshold 0.5; Luna refusals (None) are excluded and counted.

  python audit_score.py --audit-dir C:/cca/<brand>/research/count/audit_amazon --counter-out C:/cca/<brand>/research/count/out_amazon [--only-themes a,b]

audit folder holds: audit_reviews.json, manifest.json (audit id -> source_id), themes.json, the three label files.
counter-out holds theme_answers.json (Jev and Luna probabilities per row id). Writes audit_results.md and audit_results.json into the audit folder.
"""
import json, os, sys, io, argparse, statistics

try:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except Exception:
    pass


def prf(tp, fp, fn):
    p = tp / (tp + fp) if tp + fp else None
    r = tp / (tp + fn) if tp + fn else None
    f = 2 * p * r / (p + r) if p and r else (0.0 if (tp + fp + fn) else None)
    return p, r, f


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--audit-dir', required=True)
    ap.add_argument('--counter-out', required=True)
    ap.add_argument('--only-themes', default='')
    a = ap.parse_args()
    D = a.audit_dir.rstrip('/\\') + '/'
    themes = json.load(open(D + 'themes.json', encoding='utf-8'))
    only = [t for t in a.only_themes.split(',') if t] or list(themes)
    man = json.load(open(D + 'manifest.json', encoding='utf-8'))
    N = len(man)
    labs, langs = {}, {}
    for nm in ('claude_sub', 'mini', 'claude_main'):
        fn = D + {'claude_sub': 'labels_claude_sub.json', 'mini': 'labels_mini.json', 'claude_main': 'labels_claude_main.json'}[nm]
        if not os.path.exists(fn):
            sys.exit('key incomplete: missing ' + fn)
        d = json.load(open(fn, encoding='utf-8'))
        labs[nm] = {x['id']: set(x['yes']) for x in d['labels']}
        langs[nm] = {x['id']: x.get('language') for x in d['labels']}
        assert sorted(labs[nm]) == list(range(N)), nm + ' does not cover every audit id'
    ans = {x['id']: x['answers'] for x in json.load(open(a.counter_out.rstrip('/\\') + '/theme_answers.json', encoding='utf-8'))}
    votes = {(i, t): sum(1 for L in labs.values() if t in L[i]) for i in range(N) for t in only}
    key = {k: v >= 2 for k, v in votes.items()}
    unan = {k: v in (0, 3) for k, v in votes.items()}
    out_lines = ['# Blind audit results (%d texts; key = majority of 3 labellers; models at threshold 0.5)' % N, '']
    names = list(labs)
    out_lines.append('Labeller agreement (raw agreement over all answers, and agreement on positives):')
    for x in range(3):
        for y in range(x + 1, 3):
            A, B = labs[names[x]], labs[names[y]]
            agree = sum((t in A[i]) == (t in B[i]) for i in range(N) for t in only)
            both = sum((t in A[i]) and (t in B[i]) for i in range(N) for t in only)
            either = sum((t in A[i]) or (t in B[i]) for i in range(N) for t in only)
            out_lines.append('- %s vs %s: %.1f%% raw, %.1f%% on positives (%d of %d)' % (names[x], names[y], 100.0 * agree / (N * len(only)), 100.0 * both / max(1, either), both, either))
    out_lines.append('- unanimous answers: %.1f%% (%d of %d)' % (100.0 * sum(unan.values()) / len(unan), sum(unan.values()), len(unan)))
    out_lines += ['', '| Theme | Key + | Jev pred + | Jev prec | Jev recall | Jev F1 | Jev share err (pts) | Jev middle band | Luna prec | Luna recall | Luna refused | Verdict (Jev counts) |', '|---|---|---|---|---|---|---|---|---|---|---|---|']
    res = {}
    f1s = []
    for t in only:
        kp = sum(key[(i, t)] for i in range(N))
        row = {}
        for model in ('jev', 'luna'):
            tp = fp = fn = tn = ref = mid = 0
            for i in range(N):
                p = ans[man[i]['source_id']][t][model]
                if p is None:
                    ref += 1
                    continue
                if 0.25 <= p <= 0.75:
                    mid += 1
                y = key[(i, t)]
                yh = p >= 0.5
                tp += yh and y
                fp += yh and not y
                fn += (not yh) and y
                tn += (not yh) and not y
            P, R, F = prf(tp, fp, fn)
            n = tp + fp + fn + tn
            row[model] = {'tp': tp, 'fp': fp, 'fn': fn, 'P': P, 'R': R, 'F1': F, 'pred_pos': tp + fp, 'share_err': 100.0 * ((tp + fp) - (tp + fn)) / n if n else None, 'refused': ref, 'middle': mid}
        j = row['jev']
        if kp < 5:
            verdict = 'UNTESTED (%d key positives)' % kp
        elif j['P'] is not None and j['P'] >= 0.75 and abs(j['share_err']) <= 5:
            verdict = 'CLEARED'
        else:
            verdict = 'NOT CLEARED (precision %s, share error %.1f)' % ('-' if j['P'] is None else '%.2f' % j['P'], j['share_err'] or 0)
        if kp >= 8 and j['F1'] is not None:
            f1s.append(j['F1'])
        res[t] = {'key_pos': kp, 'jev': j, 'luna': row['luna'], 'verdict': verdict}
        fm = lambda v, d=2: '-' if v is None else ('%.*f' % (d, v))
        l = row['luna']
        out_lines.append('| %s | %d | %d | %s | %s | %s | %s | %d | %s | %s | %d | %s |' % (t, kp, j['pred_pos'], fm(j['P']), fm(j['R']), fm(j['F1']), fm(j['share_err'], 1), j['middle'], fm(l['P']), fm(l['R']), l['refused'], verdict))
    cleared = [t for t in only if res[t]['verdict'] == 'CLEARED']
    untested = [t for t in only if res[t]['verdict'].startswith('UNTESTED')]
    out_lines += ['', 'Cleared for counting (%d): %s' % (len(cleared), ', '.join(cleared)), 'Not cleared: %s' % ', '.join(t for t in only if t not in cleared and t not in untested),
                  'Untested (fewer than 5 key positives): %s' % ', '.join(untested)]
    if f1s:
        out_lines.append('Jev macro-F1 over themes with >= 8 key positives: %.2f (%d themes)' % (statistics.mean(f1s), len(f1s)))
    open(D + 'audit_results.md', 'w', encoding='utf-8').write('\n'.join(out_lines) + '\n')
    json.dump({'cleared': cleared, 'untested': untested, 'themes': res}, open(D + 'audit_results.json', 'w', encoding='utf-8'), indent=1)
    print('\n'.join(out_lines))


if __name__ == '__main__':
    main()
