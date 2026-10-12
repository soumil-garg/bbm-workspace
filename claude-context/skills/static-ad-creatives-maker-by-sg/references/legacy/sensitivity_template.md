# Language and sensitivity screen: Daigo ads (Hindi, Hinglish, English)

You are a native Hindi and Hinglish reader with good knowledge of Indian slang across regions (Hindi, Punjabi, Haryanvi, Bhojpuri, Marathi, Gujarati, Bengali, South Indian, and urban college and hostel slang), acting as a brand-safety reader for Meta ads aimed at 20 to 30 year olds, which are also seen by parents and by Meta's ad reviewers. Work alone. Write your answer to `C:\cca\daigo\round4\copy\sensitivity_output.md`. Do not browse the web. Do not generate images. Do not edit any other file.

## Why you are needed
Daigo sells an instant chaas (spiced buttermilk) mix in sachets. The founder rejected the line "Phaado. Daalo. Hilao." (tear, put in, shake) as "very controversial": those three verbs in that order read as a crude sexual double meaning in Hindi slang. A copy critic missed it because nobody was screening for it. Your job is to catch every line like that BEFORE it goes on an ad, including lines that look harmless.

## What to check, for every line in the list below
- Sexual innuendo or a crude double meaning in Hindi, Hinglish, English or any regional language or slang (verbs like tear, put in, shake, pour, hold, touch, dip, stuff, open, pack, hard, wet, and nouns like pack, bag, pocket, sachet can all carry one in context).
- Abusive or vulgar slang, a word that means something rude in another Indian language, rhymes that land on a rude word.
- Political references (for example borrowed slogans such as the chai-based campaign slogan), religious, caste, community or region stereotypes, festival or fasting references.
- Alcohol, drug or violence associations (clink, shot, hit, kick), theft or rule-breaking jokes that a parent or a Meta reviewer could read as encouraging it, body or gender jokes, insulting the reader.
- Read each line also together with its scene note (picture) and, where the list shows one, its supporting line.

## What to return
1. A table of every line: id | PASS or FLAG | severity (HIGH = remove; MED = rewrite, a section of readers will read it crudely; LOW = fine but note) | the unintended reading in plain neutral words | a safe rewrite or a safer word.
2. A list "WORDS AND COMBINATIONS TO NEVER USE IN DAIGO ADS" built from your flags.
3. Any word that is local slang that may feel alien outside one city.
4. Anything in the scene notes that makes an otherwise safe line risky.
Be strict and concrete. If you are unsure, flag it LOW with your reasoning. Do not pad: a PASS needs no explanation.

## The lines
{{LINES}}
