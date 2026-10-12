---
name: feedback-whole-ad-generation-harmony
description: "2026-10-10: Soumil rejected Daigo round 2 (product and text pasted on a picture, headline/picture/product not in harmony, plain sachets look like condom packs); rules: the model draws the whole ad from real refs, one story, branded sachets; his approved ads are designed studio posters, not candid UGC"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b3607133-6288-42df-85dd-d0d6d53e5a58
  modified: 2026-10-10T12:29:57.489Z
---

On 10 Oct 2026 Soumil rejected Daigo round 2 (16 creatives): "it looks like you've just pasted the product and text on pic, hate it man, really hate em ... see the approved ones and then see how they are constructed and then reverse engineer them, especially the graphic principles and quality thing", plus "the copywriting is a little better now but there is no harmony in what the text says and then what the image shows and then the product placement, also why are the sachets non branded, they look like condom packs". He also asked to see the exact prompts I gave the model.

**Why (my causes, confirmed by the prompt files):** the model got no reference image; prompts said every sachet is "completely plain" (so it drew square plain packets); the scene left empty corners for a pack that code pasted on later on a white die-cut tile; the scene was written without the headline.

**How to apply:**
1. For brand ads the image model draws the WHOLE ad (scene, real pack, sachets, headline, badges) from reference images of the real product; code compositing (render_ad.py, pack cut-outs, die-cut tiles) is only for edits, resizes and long text. Recipe: [[reference-whole-ad-generation-recipe]].
2. Write each concept as ONE story: the picture demonstrates the headline (ticket stamped CNF beside the chaas, three steps drawn as three steps) and the product takes part in it. In his approved ads 65% demonstrate a benefit and 29% depict literally; the disapproved are the reverse (67% literal).
3. Sachets are branded slim stick packs (silver crimped ends, blue front, daigo wordmark), never plain or square. Pouch reference = the real pack with claim badges removed.
4. His taste is data, not a guess: designed, studio-lit posters on a flat or built colour field, a hero cluster with a believable shadow, a headline with a typographic treatment, a concrete number. "Real people / candid UGC" is NOT supported by the 65 approved ads (people 40% approved vs 38% disapproved; candid real-scene photos 42% vs 58%). Table: vault `Resources/Ad Inspiration/Approved ads - how they are built.md`.
5. When he asks "what did you tell the model", show the exact prompts (saved next to the images as PROMPTS_roundN_exact.md) and name the sentences that caused the fault.
6. Check OpenAI credit before a run: the ledger balance is a manual estimate and was wrong on 10 Oct ([[project-daigo-pilot-oct2026]]).

Confirmed later on 10 Oct: on seeing round 3 he said the graphic designs are "really, really better than before, almost like the ones I expect you to make". Whole-ad generation is the method to keep; his remaining complaints were the copy ([[feedback-daigo-copy-both-languages-double-meaning]]).

Builds on [[feedback-daigo-round1-rejected]] (voice first stays) and [[project-swipe-desk]].
