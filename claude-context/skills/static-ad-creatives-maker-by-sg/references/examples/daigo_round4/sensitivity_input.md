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
### K CALIBRATION (lines already known to be a problem or already used; confirm you catch them)

- K.1 [HG] Phaado. Daalo. Hilao. Chaas.   (picture: hands tearing a sachet over a shaker)
- K.2 [HG] Sachet phaado. Paani daalo. Hilao.   (small supporting line under other headlines)
- K.3 [HG] Bas phaado, daalo, hilao.
- K.4 [EN] 5% OFF PREPAID. CODE PREPAY5   (offer pill)
- K.5 [EN] 10 sachet | 10 glass | Rs 279   (price strip)

### 1 TICKET
Picture: Yellow poster. A railway ticket stamped CNF lies under the pouch, one sachet lies across it like a second travel document, a full steel tumbler of chaas stands beside it.

- 1.1 [HG] Ticket confirm. Chaas confirm.
- 1.2 [HG] Sleeper mein bhi chaas.
- 1.3 [HG] Train late. Chaas ready.
- 1.4 [HG] Safar lamba. Chaas ek sachet door.
- 1.5 [EN] Waitlisted? Chaas is confirmed.
- 1.6 [EN] Ticket: confirmed. Chaas: confirmed.
- 1.7 [EN] Next stop: chaas.
- 1.8 [EN] Window seat. Chaas in hand.
- 1.9 [EN] Journey sorted. Chaas sorted.
- 1.10 [EN] Train's late. Your chaas isn't.

### 2 THREE STEPS
Picture: Green poster. A sachet is tilted over a shaker bottle with powder pouring in; a steel tumbler of chaas, a spice bowl, the pouch and three sachets sit around it. Numbered 1, 2, 3 circles beside the headline.

- 2.1 [HG] Kholo. Milao. Piyo.
- 2.2 [HG] Sachet kholo. Paani milao. Shake karo.
- 2.3 [HG] Itna easy hai chaas?
- 2.4 [HG] Teen kaam. Ek glass chaas.
- 2.5 [EN] Tear. Add water. Shake. Chaas.
- 2.6 [EN] Sachet. Water. Shake. Chaas.
- 2.7 [EN] Three steps. One glass of chaas.
- 2.8 [EN] That's the whole recipe.
- 2.9 [EN] Chaas, in three steps.
- 2.10 [EN] Recipe: water. And a sachet.

### 3 PRICE PER GLASS
Picture: Blue studio poster. One big full glass of chaas with ten sachets and the pouch beside it; a white pill reads "10 sachet. Rs 279."

- 3.1 [HG] Rs 28 ka glass.
- 3.2 [HG] Chaas ka rate: Rs 28.
- 3.3 [HG] Rs 28. Ek glass. Bas.
- 3.4 [EN] Rs 28 a glass.
- 3.5 [EN] 10 glasses of chaas. Under Rs 300.
- 3.6 [EN] Under Rs 30 a glass.
- 3.7 [EN] Rs 28. Yes, per glass.
- 3.8 [EN] A glass of chaas for Rs 28.

### 4 HOSTEL STUDENT
Picture: Cream poster. A smug student in a blue hoodie raises a steel tumbler of chaas and the pouch toward the camera; two sachets sit in his hoodie pocket.

- 4.1 [HG] Hostel mein dahi? Mazaak mat karo.
- 4.2 [HG] Mess mein chaas nahi. Room mein hai.
- 4.3 [HG] Hostel ka kitchen band. Chaas chalu.
- 4.4 [EN] Dahi in a hostel? Cute.
- 4.5 [EN] Hostel kitchen not included. Chaas is.
- 4.6 [EN] The mess doesn't serve chaas. Your bag does.
- 4.7 [EN] Plot twist: your hostel has chaas.
- 4.8 [EN] Hostel life hack: chaas in your pocket.

### 5 PG MIXER
Picture: Split poster. Left: a dirty mixer jar full of foam with a big question mark above it. Right: a bright yellow side with the pouch, two sachets, a shaker bottle and a steel tumbler of chaas.

- 5.1 [HG] PG mein mixer kaun dhoyega?
- 5.2 [HG] Aaj mixer ki chhutti.
- 5.3 [HG] Mixer ko chhutti. Chaas sachet se.
- 5.4 [EN] Not today, mixer.
- 5.5 [EN] The mixer jar isn't washing itself.
- 5.6 [EN] Chaas, not chaos.
- 5.7 [EN] Nobody's washing that mixer.
- 5.8 [EN] Skip the mixer. Sip the chaas.
- 5.9 [EN] No mixer. No mess. Just chaas.

### 6 ROOM 204 NOTE
Picture: Warm hostel-room still life. A steel tumbler of chaas carries a handwritten masking-tape note (the headline is the note); two sachets, a notebook and pen, the pouch behind.

- 6.1 [HG] ROOM 204 KI CHAAS. HAATH MAT LAGANA.
- 6.2 [HG] Isme se ek bhi sachet gaya toh...
- 6.3 [HG] Roommate, ye mera hai.
- 6.4 [EN] ROOM 204'S CHAAS. HANDS OFF.
- 6.5 [EN] Property of Room 204. Do not touch.
- 6.6 [EN] Hands off. It's labelled.
- 6.7 [EN] Touch it and we're not roommates.

### 7 MEETING BREAK
Picture: Overhead desk flat-lay. Two hands clink two steel tumblers of chaas above a notepad, an ID lanyard and a laptop edge; the pouch and three sachets lie on the desk.

- 7.1 [HG] Meeting khatam. Chaaaas break!!!
- 7.2 [HG] Meeting khatam. Chaas shuru.
- 7.3 [HG] Office mein bhi chaas break.
- 7.4 [EN] This meeting could've been an email. This chaas couldn't.
- 7.5 [EN] Meeting over. Chaas on.
- 7.6 [EN] Chaas break. You've earned it.
- 7.7 [EN] Your desk called. It wants chaas.

### 8 ROAD TRIP
Picture: A packed backpack in an open car boot with the pouch and sachets tucked inside; a steel tumbler of chaas and a bottle beside it; a sunny highway behind.

- 8.1 [HG] Road trip? Chaas pack hai.
- 8.2 [HG] Boot mein bag. Bag mein chaas.
- 8.3 [HG] Road trip ka plan: chaas.
- 8.4 [EN] Road trip? Chaas is packed.
- 8.5 [EN] Pack light. Pack chaas.
- 8.6 [EN] Packed: playlist, snacks, chaas.
- 8.7 [EN] The boot has room for chaas.

### 9 20 PACK (OFFER)
Picture: Blue poster. Two hands reach for the same sachet in a pile of about 20 sachets; a glass of chaas stands on the left; a burst reads "20 SACHET Rs 529" and a pill reads "5% OFF PREPAID. CODE PREPAY5".

- 9.1 [HG] Sachet kam padenge? 20 ka pack lo.
- 9.2 [HG] Apna bhi, dost ka bhi: 20 sachet.
- 9.3 [HG] Roommate ka bhi hisaab. 20 ka pack.
- 9.4 [EN] Roommates exist. Get 20.
- 9.5 [EN] Stop stealing his chaas. Get 20.
- 9.6 [EN] Two hands. One sachet. Get 20.
- 9.7 [EN] 10 won't last. Get 20.
- 9.8 [EN] Share or stash? Get 20.

### 10 MUMMY CHAT
Picture: A hand holds a phone showing a three-bubble chat beside the pouch and one sachet on a wooden desk. Staged skit, no names, no review styling. Each candidate is the whole three-bubble exchange.

- 10.1 [HG] Mummy: Khana kha liya? / Me: Haan. Chaas bhi. Khud banayi, sachet se. / Mummy: Beta bada ho gaya.
- 10.2 [EN] Mummy: Did you eat? / Me: Yes. Made chaas too. / Mummy: You made it? / Me: Sachet. Water. Shake.
- 10.3 [EN] Mummy: Did you eat? / Me: Yes. Chaas too. Made it myself. / Mummy: Who is this and what did you do with my child?

### 11 GHAR DOOR
Picture: A window sill at dusk with city lights; a steel tumbler of chaas, the pouch and a sachet are within reach. Feeling only, never a taste claim.

- 11.1 [HG] Ghar door. Chaas paas.
- 11.2 [HG] Ghar se door. Chaas se nahi.
- 11.3 [HG] Door sheher, apni chaas.
- 11.4 [EN] Home is far. Chaas isn't.
- 11.5 [EN] Far from home. Close to chaas.
- 11.6 [EN] Away from home. Not away from chaas.

### 12 MESS THALI
Picture: A dull steel mess thali (rice, dal, roti) against a bright steel tumbler of chaas and the pouch with two sachets; a small supporting line sits at the bottom.

- 12.1 [HG] Mess ka khana. Apni chaas.
- 12.2 [HG] Mess mein dal. Room mein chaas.
- 12.3 [EN] Mess dinner. Own chaas.
- 12.4 [EN] The mess has dal. You have chaas.
- 12.5 [EN] Dal, rice, chaas. Sorted.

### 13 BAG OF SACHETS
Picture: Blue poster. A backpack spills sachets, with the pouch and a steel tumbler of chaas beside it; a bottom strip reads "10 sachet | 10 glass | Rs 279".

- 13.1 [HG] Bag mein chaas ki dukaan.
- 13.2 [HG] Bag mein chaas, bottle mein paani.
- 13.3 [HG] 10 glass. Ek pocket.
- 13.4 [EN] 10 glasses. One pocket.
- 13.5 [EN] A chaas shop in your bag.
- 13.6 [EN] Your bag now has a chaas counter.

### 14 NEW: EQUATION
Picture: NEW picture idea. Flat colour poster drawn as an equation: a sachet, plus a glass of water, equals a glass of chaas. Defines the product for a stranger.

- 14.1 [EN] Sachet + water = chaas.
- 14.2 [EN] 1 sachet + water = 1 glass of chaas.
- 14.3 [EN] The easiest maths you'll do today.
- 14.4 [HG] Ek sachet + paani = ek glass chaas.
- 14.5 [HG] Chaas ka formula: sachet + paani.

### 15 NEW: BHAI CHAAS HAI
Picture: NEW picture idea. Two friends at a table; one asks, the other pulls a sachet out of a bag; the pouch stands on the table.

- 15.1 [HG] Bhai, chaas hai? Haan. Bag mein.
- 15.2 [HG] Chaas chahiye? Bag mein hai.
- 15.3 [EN] Got chaas? Always.
- 15.4 [EN] Got chaas? Check the bag.

### 16 NEW: POCKET SIZE
Picture: NEW picture idea. A hand holds one slim sachet like a pen against a flat colour field, the pouch behind it. Uses the verified "pocket-size sachet".

- 16.1 [EN] Chaas that fits your pocket.
- 16.2 [EN] Pocket-sized chaas.
- 16.3 [EN] Chaas, now pocket-sized.
- 16.4 [HG] Jeb mein chaas.
- 16.5 [HG] Chaas ab jeb mein.

### 17 NEW: LOUD SHOUT
Picture: NEW picture idea. A big pile of sachets with a chaas splash, one stretched-letter shout over it (the approved "SOOOOOOOO MUCH WATER!!!" energy).

- 17.1 [EN] SOOOO MUCH CHAAS!!!
- 17.2 [EN] CHAAAAAS!!!

### 18 NEW: NO X, JUST Y
Picture: NEW picture idea. Blue type-led poster with a glass and the pouch; the headline is three bold lines.

- 18.1 [HG] Dahi nahi. Mixer nahi. Jhanjhat nahi.
- 18.2 [HG] Dahi set karne ka time nahi.
- 18.3 [EN] No dahi to set. No mixer to wash.
- 18.4 [EN] Chaas without the chores.
- 18.5 [EN] Chaas. Minus the mess.
- 18.6 [EN] Skip the setting. Skip the mixing. Sip.

### S SUPPORTING LINES

- S.1 [EN] Tear. Add water. Shake.
- S.2 [EN] Tear. Shake. Sip.
- S.3 [EN] Sachet. Water. Shake.
- S.4 [EN] One sachet. One glass.
- S.5 [HG] Sachet kholo. Paani milao. Shake karo.
- S.6 [HG] Ek sachet, ek glass.

