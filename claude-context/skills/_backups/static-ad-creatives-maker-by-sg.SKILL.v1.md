---
name: static-ad-creatives-maker-by-sg
description: "Static ad creatives maker - BY SG. Soumil's end-to-end method for making Meta static ad creatives for any D2C brand: consumer-voice research (Amazon/Quora reviews), brand claims, competitor statics from Meta Ad Library, arcads-style templated prompts, generation in the user's ChatGPT Plus via Claude in Chrome, and full-res download to the Desktop. Use when Soumil asks to make/create static ads, ad creatives, image ads or statics for a brand/product."
---

# Static ad creatives maker - BY SG

Three layers, always in this order:
1. What customers actually say (their words, their problems).
2. What the brand actually provides (claims, reviews, product look).
3. The ad: short sharp headline + image, built on an arcads template.

The user dislikes clay/diorama styles and generic "brand DNA" template output (DV0x and Static-Ads repos were tested and rejected, 28 Sep 2026). Use the arcads approach only.

## Inputs to collect (ask only for what is missing)
Required:
- Brand website URL and the specific product (one product per run).
Optional, use if given:
- Meta ad account ID (to see which existing ads win), reference ads the user likes (screenshots/links), competitors to study, target city/audience, any claims that must not be used, how many ads (default 9).
Always confirm which ChatGPT Chrome profile has Plus before generating.

## Step 1: Consumer voice research
- Amazon.in reviews of the brand AND 8-12 competing products in the category. Read via Claude in Chrome: `fetch('/product-reviews/<ASIN>/?filterByStar=critical&sortBy=helpful')` + `positive`, parse `[data-hook="review"]` with DOMParser, return in chunks under ~900 chars (tool output truncates).
- Quora (logged-out is low signal; skim only). Reddit blocks Anthropic on every route; if the user wants Reddit, ask them to paste thread text.
- Output: top 8-10 pains/desires, each with 1-3 verbatim quotes and the exact words people use for the category (e.g. in India men say "deo" and "perfume", never "body spray"). Verify local terminology with a web search before writing copy.

## Step 2: Brand layer
- Shopify stores: `<site>/products.json` and `<site>/products/<handle>.json` for price, compare-at price, description, image URLs. Download product images to a working folder and view a contact sheet.
- Pick the cleanest packshot (product + label clearly visible, plain background) as THE reference image for every generation.
- List: claims on site and packaging, real review quotes (with names only if the brand shows them), price, what the existing winning ads say (pull from the ad account if given).
- Never invent claims, stats or testimonials. Real reviews only, attributed as the source shows.

## Step 3: Competitor statics
- Meta Ad Library (`ads_library_search` for page IDs, then Chrome `facebook.com/ads/library/?view_all_page_id=<id>&media_type=image&sort_data[mode]=total_impressions`). Note formats and angles that big spenders run. The Ad Library page is heavy and can freeze Chrome; keep it to a few advertisers.
- Also borrow proven category playbooks (e.g. value-counting, annotated product on clothes, luxury ingredient still life).

## Step 4: Write 9 concepts in 3 batches (3 each)
- Batch A, consumer voice: headlines built from verbatim complaints/desires.
- Batch B, competitor-inspired: formats lifted from Step 3, rebuilt for this brand.
- Batch C, real people: photoreal, scroll-stopping, local setting (e.g. Mumbai local train, office, home bathroom, date night), product as inset or in hand.
- Map each to a template in `references/arcads-prompt-library.md` (T1-T39), e.g. comment thread, bold typography hero, handwritten testimonial, annotated callouts, big stat, comparison table, pain checklist, weather-app UI, before/after.
- Headlines: 2-6 words, punchy, native to the market's language, one idea. Examples that landed: "GONE BY LUNCH? NOT THIS." / "ARMS UP. ZERO PANIC." / "1 SWIPE AT 8 AM. STILL OUD AT 8 PM." / "She leaned in. That's the oud." / "₹6 a day. Less than your cutting chai."

## Step 5: Prompt construction (one paragraph, no line breaks)
- Prefix: "Generate an image. The attached photo is the exact product reference (<PRODUCT + visual description>). Reproduce the product and its label faithfully wherever it appears."
- Body: format "1:1 static ad creative, 1080x1080", layout by section with % heights, exact text in quotes, colours as hex, fonts described.
- Real-people prompts add: "PHOTOREALISM: full-frame camera, 35/50mm, natural skin texture with pores, real fabric creases, true-to-life lighting, slight grain. Must look like a real unretouched photograph of real people, not CGI. <local ethnicity> subjects."
- Always append the three suffixes from `references/safety-suffixes.md` (no platform chrome, edge-safe 84%, text fidelity).
- Never use real people's photos from Google (likeness/copyright); generate people instead.
- Save prompts as `<working>/p/<ID>.txt` via a small python script (see `references/example-mufasa-prompts.py`).

## Step 6: Generate in ChatGPT (Claude in Chrome)
- Use the Chrome profile logged into ChatGPT Plus (`list_connected_browsers` / `select_browser`). If Grammarly is active on chatgpt.com, ask the user to turn it off (it freezes long prompts).
- Per image, new chat: navigate `https://chatgpt.com/` -> `find` "Attach photos file input button, and Ask ChatGPT textbox" -> `file_upload` the reference -> screenshot (focuses tab) -> PowerShell `Set-Clipboard -Value (Get-Content -Raw -Encoding UTF8 <file>)` -> click textbox ref -> ctrl+v -> verify via JS that `[contenteditable="true"]` text contains the prompt exactly once (clear with ctrl+a, Delete and re-paste if doubled) -> Return.
- Run up to 3 tabs in parallel. Done check: an `<img>` with naturalWidth >= 1200 exists in the chat.
- Never type long prompts keystroke by keystroke.
- To preview: overlay the image full-viewport with JS and `zoom` a region inside the viewport.

## Step 7: Download (needs the user's OK once per session)
- User must allow chatgpt.com to download multiple files in Chrome.
- In a chatgpt.com tab, for each chat ID: `fetch('/api/auth/session')` for the token, `GET /backend-api/conversation/<id>`, take the last assistant `asset_pointer`, `GET /backend-api/files/download/<file-id>?conversation_id=<id>`, fetch `download_url` as a blob, trigger an `<a download="<Brand>_<ID>_<Name>.png">` click, 800 ms apart.
- Move files from Downloads to `C:\Users\soumi\OneDrive\Desktop\<Brand> Ads\` and list them with sizes.

## Step 8: Report and save
- Reply: Desktop folder path first, then the table of ads (ID, batch, headline, one-line verdict for the ones you checked), what could not be checked, and your top 3-4 picks to run.
- Save research + concepts to the vault: `C:\Users\soumi\Documents\Vault\Projects\<brand>-ai-creatives-<mon><yyyy>.md`.
- Future add-on (not built yet): a pessimistic senior copywriter agent that critiques every headline/prompt before generation.

## References
- `references/arcads-prompt-library.md`: 37 templates with placeholders and model notes (MIT, Kruse Media).
- `references/safety-suffixes.md`: the three always-on guards.
- `references/gpt-image-guide.md`: what ChatGPT's image model does well and badly.
- `references/ad-clone-guide.md`: turn any reference ad the user sends into a reusable template (strip the other brand, keep the structure, validate by generating).
- `references/example-mufasa-prompts.py`: a complete worked example (Mufasa Man Oud Deo Stick, 9 prompts).
