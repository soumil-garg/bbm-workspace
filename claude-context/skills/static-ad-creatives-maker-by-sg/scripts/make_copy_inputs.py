"""make_copy_inputs.py: build the two briefs of the copy gate (Gate 2) from a pool and a facts file (v3, 2026-10-10).
  python <skill>/scripts/make_copy_inputs.py --pool <pool.json> --facts <copy_facts.md> --out <dir> --brand <Brand> --round <N>
        [--languages "Hinglish and English"] [--reader hindi|generic] [--swipe] [--calibration "known-bad line" ...] [--extra <file.md>]

Writes <dir>/critic_input.md (independent critic: scores every line, picks, recommends a set) and <dir>/sensitivity_input.md (native reader: slang and double-meaning screen).
  --languages  one or more languages, e.g. "English" or "Hinglish and English" or "Spanish and English". One language: the critic picks BEST and ALT and there is no mix rule.
               Two or more: the critic picks the best line per language and the recommended set mixes them roughly half and half.
  --reader     hindi = a native Hindi and Hinglish reader (the Indian market; default when a language is Hinglish or Hindi, with the known-bad Daigo calibration lines);
               generic = a native reader of the stated languages (any other market; no calibration lines unless you pass --calibration).
  --swipe      puts Soumil's approved and disapproved headlines from the Swipe Desk (C:/cca/inspiration/swipe/analysis/construction.json) into the critic brief.
  --extra      a markdown file appended to the critic brief: competitor headlines, claim register rows, the awareness level, the cold read the concept sheet gave.
Formats: references/templates/pool.example.json and copy_facts.example.md (Daigo round 4). The facts file has four sections: BLURB, WHY, FACTS, BANNED (a heading may carry a note after the word).
For a FIRST round the pictures do not exist yet: write each concept's "scene" as the proposed picture idea and delete any sentence in the blurb that says the picture is already designed.

THEN spawn two fresh general-purpose agents in parallel, in the background (neither may be the author of the lines):
  critic : "Read <dir>/critic_input.md completely and follow it; write <dir>/critic_output.md; summary of at most 120 words."
  reader : "Read <dir>/sensitivity_input.md completely and follow it; write <dir>/sensitivity_output.md; summary of at most 120 words."
Daigo round 4: 116 lines and 18 pictures took about 36 minutes for both. Afterwards send any line you wrote yourself to the reader again (SendMessage to the same agent id): a short list takes about 2 minutes.
Reconcile the two outputs into the Gate 2 table (picture, the picture idea, one line per language, your pick, the screen verdict) and show it as plain text before any image is made."""
import argparse, json, os, re, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
TPL = os.path.normpath(HERE + '/../references/templates')
SWIPE = 'C:/cca/inspiration/swipe/analysis/construction.json'
DEFAULT_CAL = ['Phaado. Daalo. Hilao. Chaas.', 'Sachet phaado. Paani daalo. Hilao.', 'Bas phaado, daalo, hilao.']

HINDI_READER = ('a native Hindi and Hinglish reader with good knowledge of Indian slang across regions (Hindi, Punjabi, Haryanvi, Bhojpuri, Marathi, Gujarati, Bengali, South Indian, and urban college and hostel slang)')
HINDI_WHY = ('The founder rejected the line "Phaado. Daalo. Hilao." (tear, put in, shake) as "very controversial": those three verbs in that order read as a crude sexual double meaning in Hindi slang. '
             'A copy critic missed it because nobody was screening for it.')
GENERIC_WHY = 'A copy critic can miss a double meaning because nobody screens for it, and a line the founder has to reject after production costs a whole round.'


def sections(path):
    t = open(path, encoding='utf-8').read()
    out = {}
    for m in re.finditer(r'^## (BLURB|WHY|FACTS|BANNED)\b[^\n]*\n(.*?)(?=^## |\Z)', t, re.S | re.M):
        out[m.group(1)] = m.group(2).strip()
    for k in ('BLURB', 'WHY', 'FACTS', 'BANNED'):
        if k not in out:
            raise SystemExit('facts file lacks the section "## %s"' % k)
    return out


def pool_md(pool):
    o = []
    for c in pool['concepts']:
        o.append('### %d %s%s' % (c['n'], c['name'], ' (NEW picture idea)' if c.get('new') else ''))
        o.append('Picture: ' + c['scene'])
        o.append('')
        for i, (lang, text, note) in enumerate(c['c'], 1):
            o.append('- %d.%d [%s] %s%s' % (c['n'], i, lang, text, ('   (' + note + ' line)') if note else ''))
        o.append('')
    o.append('### S SUPPORTING LINE (the small line at the bottom of some posters)')
    o.append('')
    for i, (lang, text, note) in enumerate(pool.get('sublines', []), 1):
        o.append('- S.%d [%s] %s%s' % (i, lang, text, ('   (' + note + ')') if note else ''))
    o.append('')
    return '\n'.join(o)


def lines_md(pool, cal):
    o = []
    if cal:
        o += ['### K CALIBRATION (known problems; confirm you catch them)', '']
        for i, t in enumerate(cal, 1):
            o.append('- K.%d %s' % (i, t))
        o.append('')
    for c in pool['concepts']:
        o.append('### %d %s' % (c['n'], c['name']))
        o.append('Picture: ' + c['scene'])
        o.append('')
        for i, (lang, text, note) in enumerate(c['c'], 1):
            o.append('- %d.%d [%s] %s' % (c['n'], i, lang, text))
        o.append('')
    o.append('### S SUPPORTING LINES')
    o.append('')
    for i, (lang, text, note) in enumerate(pool.get('sublines', []), 1):
        o.append('- S.%d [%s] %s' % (i, lang, text))
    o.append('')
    return '\n'.join(o)


def swipe_md():
    if not os.path.exists(SWIPE):
        return '(No Swipe Desk data found; calibrate on the approved ads in Resources/Ad Inspiration/Swipe Taste Profile.md.)'
    R = json.load(open(SWIPE, encoding='utf-8'))
    A = [r for r in R if r['decision'] == 'approve']
    X = [r for r in R if r['decision'] == 'reject']
    hs = lambda rows, n: [r['headline'].replace('\n', ' ').strip() for r in rows if r.get('headline') and 2 <= len(r['headline'].split()) <= 14 and '{{' not in r['headline']][:n]
    med = statistics.median([r['headline_words'] for r in A if isinstance(r.get('headline_words'), int)] or [4])
    return ('- What he APPROVES (%d approved of %d swipes in his Swipe Desk, mostly English headlines from Indian and US brands): %s. '
            'Patterns: contrast (X. Not Y.), exaggeration, a joke or pun, a direct question to the reader, a concrete number or price. Median approved headline is %d words.\n'
            '- What he DISAPPROVES: brand name only, store or location announcements, vague mood lines. Examples: %s.'
            % (len(A), len(R), '; '.join('"%s"' % h for h in hs(A, 26)), med, '; '.join('"%s"' % h for h in hs(X, 8))))


def fill(tpl, d):
    t = open(TPL + '/' + tpl, encoding='utf-8').read()
    for k, v in d.items():
        t = t.replace('{{%s}}' % k, v)
    left = re.findall(r'\{\{[A-Z_]+\}\}', t)
    if left:
        raise SystemExit('unfilled placeholders: %s' % left)
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--pool', required=True)
    ap.add_argument('--facts', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--brand', required=True)
    ap.add_argument('--round', required=True)
    ap.add_argument('--languages', default='Hinglish and English')
    ap.add_argument('--reader', choices=['hindi', 'generic'])
    ap.add_argument('--swipe', action='store_true')
    ap.add_argument('--calibration', action='append')
    ap.add_argument('--extra')
    a = ap.parse_args()
    pool = json.load(open(a.pool, encoding='utf-8'))
    f = sections(a.facts)
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    langs = [x.strip() for x in re.split(r',|\band\b', a.languages) if x.strip()]
    reader = a.reader or ('hindi' if any(x.lower() in ('hinglish', 'hindi') for x in langs) else 'generic')
    tags = []
    for c in pool['concepts']:
        for lang, _, _ in c['c']:
            if lang not in tags:
                tags.append(lang)
    if len(langs) <= 1:
        picks = 'Pick BEST and ALT (the best two candidates that are not a FAIL) and say why.'
        mix = '(one language: no language mix rule)'
        best_fmt = 'BEST: id. ALT: id. Why: one sentence. Own lines (if any).'
        natural = 'English that sounds like a witty local 22 year old and not an ad agency, or the local language as people actually text it, never translated or forced'
    else:
        picks = ('Pick ' + ', '.join('BEST-%s' % t for t in tags) + ' (the best candidate in each language that is not a FAIL) and say which one language you would run for this picture if only one.')
        mix = 'with a language mix of roughly half and half (never one language only)'
        best_fmt = ' '.join('BEST-%s: id.' % t for t in tags) + ' Run: ' + ' or '.join(tags) + '. Why: one sentence. Own lines (if any).'
        natural = 'the local language as people text it, not translated or forced, or English that sounds like a witty local 22 year old and not an ad agency'
    cal = a.calibration if a.calibration else (DEFAULT_CAL if reader == 'hindi' else [])
    extra = ''
    if a.extra:
        extra = '\n## Extra context (competitor headlines, claim register rows, awareness level, cold reads)\n' + open(a.extra, encoding='utf-8').read().strip() + '\n'
    d = dict(BRAND=a.brand, ROUND=a.round, LANGUAGES=a.languages, OUT_DIR=out.replace('/', '\\'), BLURB=f['BLURB'], WHY=f['WHY'], FACTS=f['FACTS'], BANNED=f['BANNED'],
             APPROVED_PATTERNS=swipe_md() if a.swipe else '', PICKS=picks, MIX_RULE=mix, BEST_FORMAT=best_fmt, NATURAL_RULE=natural, EXTRA=extra,
             READER_PROFILE=HINDI_READER if reader == 'hindi' else 'a native reader of %s with good knowledge of regional slang, local sensitivities, religion, politics and rude double meanings in this market' % a.languages,
             WHY_READER=HINDI_WHY if reader == 'hindi' else GENERIC_WHY,
             CAL_NOTE='Lines marked K are calibration lines that are known problems: catch them.' if cal else '')
    open(out + '/critic_input.md', 'w', encoding='utf-8').write(fill('critic_template.md', dict(d, POOL=pool_md(pool))))
    open(out + '/sensitivity_input.md', 'w', encoding='utf-8').write(fill('sensitivity_template.md', dict(d, LINES=lines_md(pool, cal))))
    n = sum(len(c['c']) for c in pool['concepts'])
    print('wrote critic_input.md and sensitivity_input.md in', out, '| concepts', len(pool['concepts']), '| candidate lines', n, '| reader', reader, '| languages', langs)
    print('NEXT: spawn the critic and the native reader as two fresh background agents (see the docstring).')


if __name__ == '__main__':
    main()
