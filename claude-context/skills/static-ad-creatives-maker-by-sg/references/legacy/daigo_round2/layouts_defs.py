# executed inside layouts_round2.py (shares its helpers). Final layouts of round 2 (10 Oct 2026).
# T = typed arm (code text in brand fonts on a band or a plate); L = lettered arm (the model drew the headline as part of the poster; code adds the real pack and the logo).

def band_layout(cid, scene_id, band='navy', fg='$white', em='$jaljira_yellow', band_pct=31, pos='top', pack_xy=(66, 72), pack_w=29, pack_rot=3, glow_xy=(82, 88),
                logo_kind='white', logo_xy=(77, 23.4), logo_w=16, extra=None, hsize=None, rule=True):
    """headline band on top (solid brand colour), the photo below it (cropped), pack bottom right, logo in the band.
    The band and its rule are raw html layers inside `images`, so the logo (a later layer) sits on top of them."""
    c = COPY2[cid]
    photo_h = 100 - band_pct
    bandhtml = {'html': '<div style="position:absolute;left:0;top:0;width:100%%;height:%s%%;background:%s"></div>' % (band_pct, tok(band))}
    rulehtml = {'html': '<div style="position:absolute;left:0;top:%s%%;width:100%%;height:1.2%%;background:%s"></div>' % (band_pct - 0.6, tok('jaljira_yellow' if band != 'jaljira_yellow' else 'navy'))}
    ims = [{'src': scene(scene_id), 'x': 0, 'y': band_pct, 'w': 100, 'css': 'height:%s%%;object-fit:cover;object-position:%s;' % (photo_h, pos)}, bandhtml] + ([rulehtml] if rule else []) + [
        outline(pack_xy[0], pack_xy[1], pack_w, pack_rot), pack(pack_xy[0], pack_xy[1], pack_w, pack_rot), logo(logo_xy[0], logo_xy[1], logo_w, logo_kind)]
    items = [{'text': hl(c, em), 'size': hsize or (9.0 if len(c['h']) == 2 else 7.6), 'font': 'Baloo 2', 'weight': 800, 'color': fg, 'line': 0.98}]
    if c.get('sub'):
        items.append({'text': c['sub'], 'size': 3.3, 'font': 'Poppins', 'weight': 600, 'color': fg, 'gap': 1.6})
    return base(bg_color='$navy', images=ims, elements=list(extra or []), stacks=[{'x': 7, 'y': 8, 'w': 86, 'items': items}])


def poster_layout(cid, scene_id, ims_after=(), els=(), scr=None, hsize=9.4, fg='$white', em='$jaljira_yellow', sub_color='$white', sub_size=3.4, sub_gap=2.2, stack_xyw=(7, 8, 86), headline_css=''):
    """full-bleed photo with the headline set on a calm part of the picture; optional scrim"""
    c = COPY2[cid]
    items = [{'text': hl(c, em), 'size': hsize, 'font': 'Baloo 2', 'weight': 800, 'color': fg, 'line': 0.98, 'css': headline_css}]
    if c.get('sub'):
        items.append({'text': c['sub'], 'size': sub_size, 'font': 'Poppins', 'weight': 600, 'color': sub_color, 'gap': sub_gap})
    return base(bg=scene(scene_id), images=list(ims_after), elements=([scr] if scr else []) + list(els), stacks=[{'x': stack_xyw[0], 'y': stack_xyw[1], 'w': stack_xyw[2], 'items': items}])


def lettered(sid, pack_xy=(66, 72), pack_w=29, logo_xy=(7, 85), glow_xy=(82, 88)):
    """lettered arm: the model drew the headline as part of the poster; code adds only the real pack and the logo"""
    return base(bg=scene(sid), images=[outline(pack_xy[0], pack_xy[1], pack_w, 3), pack(pack_xy[0], pack_xy[1], pack_w, 3), logo(logo_xy[0], logo_xy[1], 21, 'white')])


# ---------------------------------------------------------------- typed arm
def T_hostel():
    return band_layout('C1b', 'S1_Hostel', band='navy', pack_xy=(67, 71), pack_w=28, hsize=8.4)


def T_train():
    return band_layout('C2b', 'S2_Train', band='chaas_green', fg='$navy', em='$navy', pos='center', pack_xy=(64, 71), pack_w=30, logo_kind='blue', logo_xy=(76, 21.5), logo_w=17, hsize=8.4)


def T_pg():
    return band_layout('C3', 'S3_PGKitchen', band='jaljira_yellow', fg='$navy', em='$magenta', pack_xy=(66, 72), pack_w=29, logo_kind='blue', logo_xy=(76, 21.5), logo_w=17, hsize=8.4)


def T_steps():
    c = COPY2['C4']
    return base(bg=scene('S4_Steps'), images=[outline(66, 72, 30, 4), pack(66, 72, 30, 4), logo(7, 84, 21, 'white')],
                elements=[{'text': '', 'x': 0, 'y': 0, 'w': 46, 'size': 1, 'css': 'height:100%;background:linear-gradient(to right, rgba(15,35,95,.55), rgba(15,35,95,0));'}],
                stacks=[{'x': 6, 'y': 8, 'w': 36, 'items': [
                    {'text': hl(c, '$jaljira_yellow'), 'size': 8.2, 'font': 'Baloo 2', 'weight': 800, 'color': '$white', 'line': 0.94, 'css': 'text-shadow:0 3px 16px rgba(0,0,0,.35);'}]}])


def T_roof():
    return poster_layout('C7b', 'S7_Rooftop', ims_after=[outline(66, 72, 29, 3), pack(66, 72, 29, 3), logo(7, 85, 21, 'white')],
                         scr=scrim(46, True, 0.55, '40,20,30'), hsize=9.6, headline_css='text-shadow:0 3px 18px rgba(0,0,0,.45);')


def T_bag():
    c = COPY2['C5']
    return base(bg=scene('S5_Bag'), images=[outline(58, 55, 38, -3), pack(58, 55, 38, -3)], elements=[strip(c['strip'], 87.5, 12.5)],
                stacks=[{'x': 52, 'y': 8, 'w': 44, 'items': [{'text': c.get('h3') or hl(c, '$white'), 'size': 9.4, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 0.96}]}])


def T_price():
    c = COPY2['C6']
    lift = {'html': '<div style="position:absolute;left:0;top:0;width:100%%;height:100%%;background:%s;mix-blend-mode:lighten"></div>' % tok('navy')}   # shadows of the studio plate rise to the kit navy (QA check 13)
    return base(bg=scene('S6_Glass'), images=[lift, outline(53, 60, 42, 4), pack(53, 60, 42, 4), logo(7, 85, 21, 'white')],
                stacks=[{'x': 44, 'y': 8, 'w': 52, 'items': [
                    {'text': c['h'][0], 'size': 19.0, 'font': 'Baloo 2', 'weight': 800, 'color': '$jaljira_yellow', 'line': 0.9},
                    {'text': c['h'][1], 'size': 8.0, 'font': 'Baloo 2', 'weight': 800, 'color': '$white', 'line': 1.0, 'gap': 0.5},
                    {'text': c['sub'], 'size': 3.8, 'font': 'Poppins', 'weight': 600, 'color': '$white', 'gap': 2.0}]}])


def T_roommates():
    return band_layout('C9', 'S9_Roommates', band='daigo_blue', pos='bottom', pack_xy=(70, 74), pack_w=26, logo_xy=(77, 23.4), logo_w=16, hsize=7.8,
                       extra=[burst([('5% OFF', 0.20), ('prepaid', 0.12), ('PREPAY5', 0.14)], 4, 73, 21, -8)])


def T_bold():
    c = COPY2['C10']
    return base(bg_color='$jaljira_yellow', images=[{'src': scene('S10_GlassYellow'), 'x': 0, 'y': 0, 'w': 100, 'css': 'transform:scaleX(-1);'}, glow(26, 80, 52, 0.7, '255,255,255'), pack(4, 62, 40, -4), logo(77, 19.5, 15, 'blue')],
                stacks=[{'x': 7, 'y': 8, 'w': 86, 'items': [
                    {'text': '<br>'.join(c['h']), 'size': 9.0, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 0.96},
                    {'text': c['sub'], 'size': 3.4, 'font': 'Poppins', 'weight': 700, 'color': '$navy', 'gap': 2.0, 'css': 'max-width:44%;'}]}])


def T_chat():
    msgs = COPY2['C11']['msgs']
    rows = ''
    for who, t in msgs:
        side = 'flex-start' if who == 'in' else 'flex-end'
        bg = tok('white') if who == 'in' else tok('green_light')
        rad = '2.2% 7% 7% 7%' if who == 'in' else '7% 2.2% 7% 7%'
        rows += ('<div style="display:flex;justify-content:%s;margin-bottom:3.4%%"><div style="max-width:80%%;background:%s;border-radius:%s;padding:3.4%% 4.6%%;font:600 %dpx Poppins;color:%s;box-shadow:0 3px 8px rgba(0,0,0,.12)">%s</div></div>'
                 % (side, bg, rad, 4.4 * 10.8, tok('ink'), t))
    head = ('<div style="display:flex;align-items:center;gap:3%%;background:%s;color:%s;padding:3%% 4%%;border-radius:4%% 4%% 0 0"><div style="width:%dpx;height:%dpx;border-radius:50%%;background:%s;color:%s;font:800 %dpx \'Baloo 2\';display:flex;align-items:center;justify-content:center">M</div>'
            '<div><div style="font:700 %dpx Poppins">Mummy</div><div style="font:500 %dpx Poppins;opacity:.8">online</div></div></div>') % (
        tok('daigo_blue'), tok('white'), 6.2 * 10.8, 6.2 * 10.8, tok('jaljira_yellow'), tok('navy'), 3.6 * 10.8, 3.8 * 10.8, 2.6 * 10.8)
    card = ('<div style="position:absolute;left:7%%;top:6%%;width:86%%;background:%s;border-radius:4%%;box-shadow:0 14px 30px rgba(0,0,0,.22)">%s<div style="padding:5%% 4.5%% 1.5%%">%s</div></div>'
            % (tok('paper'), head, rows))
    return base(bg_color='$cream', images=[{'html': card}, pack(63, 70, 32, 4), logo(7, 86, 21, 'blue')])


LAYOUTS = {
    'R2_T_Hostel': T_hostel, 'R2_T_Train': T_train, 'R2_T_PG': T_pg, 'R2_T_Steps': T_steps, 'R2_T_Roof': T_roof,
    'R2_T_Bag': T_bag, 'R2_T_Price': T_price, 'R2_T_Roommates': T_roommates, 'R2_T_Bold': T_bold, 'R2_T_Chat': T_chat,
    'R2_L_Hostel': lambda: lettered('L1_Hostel'),
    'R2_L_Train': lambda: lettered('L2_Train'),
    'R2_L_Roof': lambda: lettered('L7_Rooftop'),
    'R2_L_Note': lambda: lettered('S12_Note', pack_xy=(67, 72), pack_w=28, logo_xy=(76, 8)),
    'R2_L_Office': lambda: lettered('L13_Office'),
    'R2_L_Road': lambda: lettered('L14_Road'),
}
