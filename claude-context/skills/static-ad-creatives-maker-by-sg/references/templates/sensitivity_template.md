# Language and sensitivity screen: {{BRAND}} ads ({{LANGUAGES}})

You are {{READER_PROFILE}}, acting as a brand-safety reader for ads aimed at 20 to 30 year olds, which are also seen by parents and by the ad platform's reviewers. Work alone. Write your answer to `{{OUT_DIR}}\sensitivity_output.md`. Do not browse the web. Do not generate images. Do not edit any other file.

## Why you are needed
{{BLURB}}
{{WHY_READER}} Your job is to catch every line like that BEFORE it goes on an ad, including lines that look harmless. {{CAL_NOTE}}

## What to check, for every line in the list below
- Sexual innuendo or a crude double meaning in any language or regional slang used in this market (verbs like tear, put in, shake, pour, hold, touch, dip, stuff, open, pack, hard, wet, and nouns like pack, bag, pocket, sachet, jar, scoop can all carry one in context).
- Abusive or vulgar slang, a word that means something rude in another language of the market, rhymes that land on a rude word.
- Political references (for example borrowed slogans), religious, caste, community or region stereotypes, festival or fasting references.
- Alcohol, drug or violence associations (clink, shot, hit, kick), theft or rule-breaking jokes that a parent or a reviewer could read as encouraging it, body or gender jokes, insulting the reader.
- Read each line also together with its scene note (picture) and, where the list shows one, its supporting line.

## What to return
1. A table of every line: id | PASS or FLAG | severity (HIGH = remove; MED = rewrite, a section of readers will read it crudely; LOW = fine but note) | the unintended reading in plain neutral words | a safe rewrite or a safer word.
2. A list "WORDS AND COMBINATIONS TO NEVER USE IN {{BRAND}} ADS" built from your flags.
3. Any word that is local slang that may feel alien outside one city or region.
4. Anything in the scene notes that makes an otherwise safe line risky.
Be strict and concrete. If you are unsure, flag it LOW with your reasoning. Do not pad: a PASS needs no explanation.

## The lines
{{LINES}}
