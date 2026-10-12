---
name: feedback_image_model_default
description: For OpenAI API image generation use gpt-image-2.5-sunburst (finals) or gpt-image-2.5-flare (fast drafts), never chatgpt-image-latest. Decided by Soumil 2026-10-03 after 4-brand tests.
metadata:
  type: feedback
---

Soumil's rule (2026-10-03): from now on generate images through the OpenAI API with **gpt-image-2.5-sunburst** or **gpt-image-2.5-flare**, not chatgpt-image-latest (older, about $0.26 per 1024x1536 image, more polished and less faithful).

**Why:** tested on Lotus C06, two Savvy ads and Daigo B2 with the same prompts and reference photos. Sunburst and flare matched or beat the old model on fidelity and look, at about 1,372 to 1,756 output tokens versus 4,160 to 6,240, roughly $0.055 to $0.07 per image versus $0.18 to $0.26. gpt-image-2 was slower and dearer ($0.17 to $0.23) with no clear gain. Both 2.5 models bill the same ($5/M text in, $8/M image in, $30/M image out); flare is faster (about 25 s), sunburst slightly more detailed and ranked higher on Arena (third-party sites).

**How to apply:** default sunburst for finals, flare for fast or high-volume drafts. Use the /v1/images/edits endpoint with the real product photo attached. Watch for: lower, more revealing necklines on people shots (add "modest high-neck blouse"; flare was once blocked by moderation with safety_violations=[sexual]), and statues cropped at the plinth (add "statue smaller, full plinth visible inside the 84% safe area"). Sizes available: 1024x1024, 1024x1536, 1536x1024. API credits are prepaid: Soumil topped up $8 on 3 Oct 2026; he reported a balance of $16 on 4 Oct 2026 (his figure, not verifiable by API: the key cannot read balance and the Chrome profile is not signed in to platform.openai.com). Scripts: C:\cca\lotus-sculpture\gen.py (default now sunburst), oai.py reads OPENAI_API_KEY from the user env. Related: [[reference_chatgpt_image_pipeline]] [[client_lotus_sculpture]].
