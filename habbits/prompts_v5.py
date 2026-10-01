import sys
sys.stdout = open(__import__('os').devnull,'w')
from prompts_v4 import PRE, SUF, SYS
sys.stdout = sys.__stdout__
LEAN = " [LEAN LAYOUT - IMPORTANT] Previous version was overfilled. Keep it airy: at least 45% of the canvas is empty background. Products are SMALL inside their cards with wide padding all round. No struck-through prices, no extra lines, no footers, no icons, no decorations. Only the text listed."
SYSP = SYS['P']
P = {}
P['B2v2a_P_Combos3'] = PRE + "1:1 static ad creative, 1080x1080. Warm off-white #F4F1EC background. Top 22%: headline in huge heavy black #111111 sans-serif, centred, one line: \"ANY 3. PAY FOR 2.\" Middle 55%: three equal white rounded cards side by side with wide gaps between them and lots of empty white space inside each. Each card holds only three small products in a tight neat row in the upper part, and under them one bold title and one big price on a lime #C9F24B pill. Card 1: products Te-Cha toothpaste, Whitening Powder jar, Whitening Serum; title \"WHITENING\"; price \"₹997\". Card 2: products Te-Cha toothpaste, Charcoal Mouthwash, Copper Tongue Cleaner; title \"FRESH BREATH\"; price \"₹647\". Card 3: products Apple Mint toothpaste, Sensitivity Mouthwash, Copper Tongue Cleaner; title \"GENTLE\"; price \"₹647\". Bottom 15% empty. That is ALL the text." + LEAN + SYSP + SUF
P['B2v2b_P_Combos2'] = PRE + "1:1 static ad creative, 1080x1080. Warm off-white #F4F1EC background. Top 22%: headline in huge heavy black #111111 sans-serif, centred, one line: \"ANY 3. PAY FOR 2.\" Middle 58%: two equal white rounded cards side by side with a wide gap between them and generous empty white space inside each. Each card holds three products in a tidy row in the upper part, and under them one bold title and one big price on a lime #C9F24B pill. Card 1: products Te-Cha toothpaste, Whitening Powder jar, Whitening Serum; title \"WHITENING\"; price \"₹997\". Card 2: products Te-Cha toothpaste, Charcoal Mouthwash, Copper Tongue Cleaner; title \"FRESH BREATH\"; price \"₹647\". Bottom 12% empty. That is ALL the text." + LEAN + SYSP + SUF
for k, v in P.items():
    open(f'C:/cca/habbits/p5/{k}.txt', 'w', encoding='utf-8').write(v)
print({k: len(v) for k, v in P.items()})
