"""Prompt builder template. Copy to C:\\cca\\<brand>\\prompts.py, fill BRAND, write one entry per creative.
Run: python prompts.py  -> writes p\\<ID>.txt (one paragraph each).

ID scheme: <funnel><n>_<system>_<name>  e.g. C3_F_GroupPhoto (top funnel concept 3, face+gaze), B4_N_Cart (bottom funnel 4, native).
Systems: M minimal, T bold type, N native, F face/gaze, H product hero, P proof/data, A rich art, U ugly.
Read references/design-rules.md before writing. Text goes in double quotes, exactly as approved copy.
"""
import os

WORK = r'C:\cca\brand'          # working folder
BRAND = {
    'name': 'BRAND',
    'category': 'oral-care',    # for the prefix sentence
    # one line per product: how it looks (from the packshots). Only products used in ads.
    'products': {
        'hero': "the black tube (matte black, vertical white wordmark)",
    },
    'accent': '#C9F24B', 'dark': '#111111', 'light': '#F4F1EC',
    'pill': 'a small rounded pill badge in accent colour with black bold text "BUY 2 GET 1 FREE"',
    'locale': 'Indian subject, natural Indian skin tone',
}

PRE = ("Generate an image. The attached photo is the exact product reference sheet for the brand " + BRAND['name'] + ". "
       + " ".join(f"{k}: {v}." for k, v in BRAND['products'].items()) +
       " Reproduce every product you show exactly as in the reference: same shape, colours, wordmark, logo and label layout. "
       "Show ONLY the product containers: no props, fruit, leaves, stones, badges or 'as seen on' stickers from the reference. "
       "Do not add text to labels. Do not invent products or brands. ")

SUF = (" [NO PLATFORM CHROME] Standalone ad creative only. No phone status bar, device frame, Sponsored label, captions, like counts or app buttons unless explicitly described."
       " [EDGE-SAFE] All text and products within the central 84% of the canvas, about 8% padding from every edge."
       " [TEXT FIDELITY] Render exactly the words in double quotes, spelled exactly, with exactly these prices; no extra words, numbers or claims anywhere."
       " Inside chat bubbles or notes: plain words only, no emoji, exactly the number of messages/lines specified.")

REAL = (" PHOTOREALISM: full-frame camera, 35-50mm lens, natural skin texture with pores, real fabric creases, true-to-life light, slight grain; "
        "a real unretouched photograph, not CGI. " + BRAND['locale'] + ". Correct anatomy: exactly two arms and two hands, five fingers each. ")

SYS = {
 'M': " [DESIGN SYSTEM: MINIMAL SWISS] Premium, uncluttered. The headline is the dominant element, at least 3x larger than any other text. At least 40% empty space. No props. Warm off-white background, accent colour on one element only. Single centre axis. Soft even studio light, heavy modern grotesque sans-serif.",
 'T': " [DESIGN SYSTEM: BOLD TYPOGRAPHY] Type is the hero, filling about 60% of the canvas, heavy condensed sans-serif, tight leading, flush left. Products small (under 20% of the height) in a lower corner. Two colours plus the accent. No decorations.",
 'N': " [DESIGN SYSTEM: NATIVE LO-FI] Looks like something an ordinary person made on their phone, not an advertisement: plain default phone UI typography, no brand styling, no polish, casual phone-camera quality; blends into a social feed.",
 'F': " [DESIGN SYSTEM: FACE AND GAZE] A real person's face draws attention first; their eye-line points at the product and the offer, not at the camera. Product large and legible. Headline in clean empty space away from the face.",
 'H': " [DESIGN SYSTEM: PRODUCT HERO CONTRAST] One product or group is isolated and different from everything else so it pops. Single dramatic light source, clean deep shadows, museum-like emptiness. Minimal text.",
 'P': " [DESIGN SYSTEM: PROOF AND DATA] Clean information design; the numbers are the hero. Strict grid, precise alignment, tabular figures, generous spacing, black on warm off-white, accent only on the pay-price.",
 'A': " [DESIGN SYSTEM: RICH ART DIRECTION] Editorial magazine-quality lifestyle photograph, a fully styled real scene with warm natural light and depth. Richness lives in the image, not the text: one headline, one message.",
 'U': " [DESIGN SYSTEM: DELIBERATELY UGLY] Intentionally amateur and scrappy, like a rushed homemade post: flat phone flash, slightly crooked framing, marker handwriting or MS Paint style. Unpolished, but the headline and offer must be large and perfectly legible.",
}
LEAN = (" [LEAN LAYOUT] Keep it airy: at least 45% empty background, small products with wide padding, no struck-through prices, "
        "no extra lines, footers, icons or decorations. Only the text listed.")


def P_(body, system, real=False, lean=False):
    return PRE + (REAL if real else "") + "1:1 static ad creative, 1080x1080. " + body + SYS[system] + (LEAN if lean else "") + SUF


P = {}
# Example entry (replace):
# P['C1_M_Name'] = P_('Top 35%: headline in huge heavy black sans-serif, two centred lines: "LINE ONE" / "LINE TWO." '
#                     'Middle 40%: the three products side by side, equal spacing. Bottom: ' + BRAND['pill'] + '. That is ALL the text.', 'M')

if __name__ == '__main__':
    out = os.path.join(WORK, 'p'); os.makedirs(out, exist_ok=True)
    for k, v in P.items():
        open(os.path.join(out, k + '.txt'), 'w', encoding='utf-8').write(v)
    print(len(P), {k: len(v) for k, v in P.items()})
