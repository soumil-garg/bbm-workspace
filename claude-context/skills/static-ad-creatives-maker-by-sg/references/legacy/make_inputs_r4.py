import sys, os
sys.path.insert(0, 'C:/cca/daigo/round4/copy')
from pool_r4 import CONCEPTS, SUBLINES

D = 'C:/cca/daigo/round4/copy/'


def pool_md():
    out = []
    for c in CONCEPTS:
        out.append('### %d %s' % (c['n'], c['name']))
        out.append('Picture: ' + c['scene'])
        out.append('')
        for i, (lang, text, note) in enumerate(c['c'], 1):
            out.append('- %d.%d [%s] %s%s' % (c['n'], i, lang, text, ('   (' + note + ' round 3 line)') if note else ''))
        out.append('')
    out.append('### S SUPPORTING LINE (the small how-to line at the bottom of some posters; it replaces the old one)')
    out.append('')
    for i, (lang, text, note) in enumerate(SUBLINES, 1):
        out.append('- S.%d [%s] %s%s' % (i, lang, text, ('   (' + note + ')') if note else ''))
    out.append('')
    return '\n'.join(out)


def lines_md():
    out = []
    out.append('### K CALIBRATION (lines already known to be a problem or already used; confirm you catch them)')
    out.append('')
    out.append('- K.1 [HG] Phaado. Daalo. Hilao. Chaas.   (picture: hands tearing a sachet over a shaker)')
    out.append('- K.2 [HG] Sachet phaado. Paani daalo. Hilao.   (small supporting line under other headlines)')
    out.append('- K.3 [HG] Bas phaado, daalo, hilao.')
    out.append('- K.4 [EN] 5% OFF PREPAID. CODE PREPAY5   (offer pill)')
    out.append('- K.5 [EN] 10 sachet | 10 glass | Rs 279   (price strip)')
    out.append('')
    for c in CONCEPTS:
        out.append('### %d %s' % (c['n'], c['name']))
        out.append('Picture: ' + c['scene'])
        out.append('')
        for i, (lang, text, note) in enumerate(c['c'], 1):
            out.append('- %d.%d [%s] %s' % (c['n'], i, lang, text))
        out.append('')
    out.append('### S SUPPORTING LINES')
    out.append('')
    for i, (lang, text, note) in enumerate(SUBLINES, 1):
        out.append('- S.%d [%s] %s' % (i, lang, text))
    out.append('')
    return '\n'.join(out)


for tmpl, key, body, outname in (('critic_template.md', '{{POOL}}', pool_md(), 'critic_input.md'),
                                 ('sensitivity_template.md', '{{LINES}}', lines_md(), 'sensitivity_input.md')):
    t = open(D + tmpl, encoding='utf-8').read()
    assert key in t
    open(D + outname, 'w', encoding='utf-8').write(t.replace(key, body))
    print('wrote', outname, len(t.replace(key, body)), 'chars')

n = sum(len(c['c']) for c in CONCEPTS)
print('concepts', len(CONCEPTS), 'candidate lines', n, 'sublines', len(SUBLINES))
