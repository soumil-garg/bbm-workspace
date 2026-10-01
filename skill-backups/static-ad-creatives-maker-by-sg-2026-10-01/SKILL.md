---
name: static-ad-creatives-maker-by-sg
description: "Static ad creatives maker - BY SG (v2, full pipeline). Soumil's end-to-end system for making Meta static ad creatives for any D2C brand: past ad data, consumer research (Amazon, Reddit, competitors), psychology (segments, offers, angles), copy from named principles with a critique pass, several design systems per idea, top-of-funnel and bottom-of-funnel sets, ChatGPT image generation via Claude in Chrome, a 10-point QA gate, approval folder, then Meta upload. Use when Soumil asks to make/create ad creatives, static ads, image ads or statics for a brand, or says 'run the ad creative system on <brand>'."
---

# Static ad creatives maker - BY SG (v2)

One rule behind everything: **every creative is a hypothesis about a specific person, a specific emotion and a specific reason to buy now.** We make the best hypotheses we can, and the ad account kills the wrong ones. Scope: D2C, static images. Tone with Soumil: direct, call him sir, have an opinion, never assume on client work.

The pipeline, in order. Do not skip a stage. Do not jump to copy or prompts before research.

| Stage | What | Output | User gate |
|---|---|---|---|
| 0 | Intake | working folder + vault note | ask only what is missing |
| 1 | Past data (Meta, Shopify) | winners, audience shifts, claims used | none |
| 2 | Market research | pains table, words, competitor-owned claims | none |
| 3 | Psychology | segments, offer bank, angles | **GATE 1: Soumil picks concepts** |
| 4 | Copy | headline + primary text, labelled, critiqued | **GATE 2: Soumil approves copy** |
| 5 | Design + prompts | several design systems per concept | none |
| 6 | Generate + download | images on Desktop | ask once before downloading |
| 7 | QA gate | pass/fail per image, regenerate fails | none |
| 8 | Deliver | For Approval folder + contact sheet | **GATE 3: feedback / approval** |
| 9 | Fix loop | local edits or regenerate | repeat until approved |
| 10 | Meta upload + tagging | ads live | only after approval |

Speak to Soumil at gates and when something blocks you. In between, work autonomously and say in one line what you are doing if a step is long.

## Stage 0: Intake
Ask only for what is missing. Required: brand + site URL. Then:
- Meta ad account ID (never assume it; confirm). Past data drives everything, so ask if none.
- Funnel stage: top (cold, problem-led), bottom (warm, offer-led), or both. Default both.
- Fixed constraints: client-mandated offer/deal (e.g. Habbits: every ad carries Buy 2 Get 1 Free), claims that must not be used, claims the brand has used before (reusable).
- Products in scope, Shopify/analytics access (optional), how many ads (default 6 concepts, 2-3 design systems each).
- Which Chrome profile has ChatGPT Plus (`list_connected_browsers`; two profiles are common, one usually holds Amazon login).

Setup:
- Working folder `C:\cca\<brand>\` with `research\`, `img\`, `p\` (prompts), `ref\`.
- Vault note `C:\Users\soumi\Documents\Vault\Projects\<brand>-creative-research-<mon><yyyy>.md` from `Templates\project.md` style (frontmatter status/priority, sections per stage, status log). Use `[[wikilinks]]`. Log every stage into it as you go.
- Read the client's existing vault note and memory file first (`client_<brand>.md`).

## Stage 1: Past data
Detail and code in `references/research-playbook.md`. Summary:
1. Account by month (`get_insights` level account, time_breakdown month, range maximum). Note eras: best period, pauses, restarts. Purchases = `omni_purchase`.
2. Ad level per era, sorted by spend, with ROAS and CTR. Big outputs are saved to a file by the tool: parse with Python (`encoding='utf-8'`).
3. `bulk_get_ad_creatives` with `fields=id,name,body,title,object_type,image_url,thumbnail_url,object_story_spec` for the top ~25 ads. Extract copy, download images, build a contact sheet, LOOK at the images.
4. Age/gender breakdown for the best era vs now. Audience drift (e.g. women dropped from 36% to 17% of spend) is a finding, not noise.
5. Shopify products.json for live prices and variants. Customer data only if access exists; if not, say so and move on (never block).
6. Write findings: hero product, what promise+proof pattern won, what lost, bundle history, claims used, drift, format saturation ("all statics look the same").
Rule: results judged by ROAS and purchases, not CTR alone (a 2.58% CTR ad had 0.82 ROAS).

## Stage 2: Market research
Detail in `references/research-playbook.md`. Sources, all of them:
- Amazon.in reviews of the brand AND 8-12 competitors, critical + 3-star + positive (script in playbook). Needs the Chrome profile logged into Amazon.
- Reddit through the Arctic Shift archive (`scripts/reddit_research.py`). Reddit is blocked directly (WebFetch, curl, Chrome). Do not ask Soumil to paste threads.
- Competitor ads: `ads_library_search`, ads live 30+ days, note formats and offers. Include category-adjacent leaders.
- Claims/safety research (regulatory or clinical facts that shape what we can say; e.g. charcoal abrasiveness).
- YouTube comments are unreliable (page freezes). Quora is low signal. Treat as optional.
Output into the vault note: 8-12 pains/desires each with HIGH/MED/LOW confidence and verbatim quotes, the words people use, claims competitors already own (do not lead with them), a strategic read (awareness and sophistication level, the honest opening).

## Stage 3: Psychology
Framework in `references/psychology-framework.md`. Vocabulary is fixed:
- **Segment** who. **Driver** what they feel. **Offer** what the creative promises (the core promise, NOT a sale or discount). **Angle** the lens/door in. **Format** how it looks. **Hook** the scroll-stopper. Concept = segment x driver x offer x angle.
- If the client fixes a deal (B2G1), the deal is constant and the **offer axis becomes "why want it"** (routine, results take weeks, moment, safe, dentist price, try it, share it).
Produce: 4-5 segments (driver, main objection, awareness level, evidence), a ranked offer bank (5-7), 3-4 angles per offer, guardrails, and a recommended round (one offer per creative, told plainly, plus one native/ugly slot). Also list what you need verified before use (claims, prices, cart rules).
**GATE 1:** show the concept sheet, recommend picks, wait for Soumil's choice or "go ahead".

## Stage 4: Copy
Principles and template in `references/copy-principles.md`. Every headline and primary text is labelled with awareness level, headline type, persuasion lever, VoC source, and reason-why. Headlines 2-6 words, in the customers' language, one idea. Then run the critique pass (clear in 2s, specific, believable, scroll-stop, brand fit, policy) and rewrite what fails. Write Meta headline + primary text (short and long) per creative. Verify every price against the live site; compute anchors/receipts yourself.
**GATE 2:** show copy, wait for approval or edits. Never invent claims, stats or testimonials. Brand-used claims are reusable when Soumil says so; timelines may be "what to expect", never fake customer quotes.

## Stage 5: Design and prompts
Rules in `references/design-rules.md` (the hard rules; read before every prompt batch). Systems in `references/design-systems.md`. Funnel differences in `references/funnel-playbook.md`.
- Render the **same copy** in 2-3 different design systems per concept, so the test isolates design. Include at least one deliberately ugly/native version per set.
- Top of funnel: problem/curiosity/proof, real people and native formats work. Bottom of funnel: the offer IS the headline, show the mechanism and the range, no problem-agitation.
- Reference image: a clean packshot-only sheet (`scripts/build_reference.py`). Props in reference photos (fruit, leaves, badges) leak into outputs, so crop them out.
- Prompt builder: copy `scripts/prompts_template.py` to `C:\cca\<brand>\prompts.py`, fill BRAND, write one prompt per creative into `p\<ID>.txt`. Always append the three suffixes (no chrome, edge-safe 84%, text fidelity). Prompt = prefix (product fidelity) + format/layout by % + exact text in quotes + colours as hex + design system block + suffixes. Keep each under about 2.8k characters.
- ID scheme: `<funnel><concept>_<system>_<name>` e.g. `C3_F_GroupPhoto`, `B4_N_Cart`.

## Stage 6: Generate and download
Exact working procedure in `references/chatgpt-pipeline.md`. Summary: per image, new chat, clipboard-paste the prompt (never type or `insertText`), attach the reference, send via the form Send button, record the chat ID. Submit all, wait about 2 minutes, then download through the backend API in one JS call. Downloads need Soumil's OK once per session: state file count, source, approximate size, destination, then wait for a yes. Destination `C:\Users\soumi\OneDrive\Desktop\<Brand> Ads\<round>\`. Close the tabs you opened and stop any background servers when done.

## Stage 7: QA gate
`references/qa-gate.md`. Build a contact sheet, view every image, zoom into anything with small text or people. Pass/fail each. Regenerate fails with a patched prompt (log the reason, keep rejects in `rejected\`). Do not show Soumil anything that fails.

## Stage 8: Deliver
- `<Brand> Ads\For Approval\` with clean names (no `_v2`), contact sheets per set.
- Tell Soumil the path and open it (`Start-Process explorer.exe <path>`; the Desktop lives in OneDrive). Send the contact sheet with SendUserFile.
- Give: what each set is, your top picks and why, what could not be verified, open questions (end dates, claim proof).
- Offer the approval pack (each image beside Meta headline + primary text) when the client needs to sign off.

## Stage 9: Fix loop
Soumil's feedback is usually specific and small. Prefer **local edits** (PIL, alpha-mask compositing, keep the original in `original\`) for text removals and re-alignments: they keep the rest of the image identical. Regenerate only for layout/imagery changes. If feedback says "overfilled", cut elements (see design rules), do not just shrink. When one image gets feedback, check the sibling images for the same flaw.

## Stage 10: Meta upload and tagging (after approval only)
- Ask before uploading anything. Use Meta MCP (`mcp__9c1ec85d...`): upload images, create creatives, ads. Multi-format = ONE ad with placement asset customization (vertical for Stories/Reels, square for Feeds), never an ad per format (memory: feedback_placement_asset_customization).
- Dropbox route for bulk: memory reference_dropbox_meta_upload.
- Name every ad with tags so results roll up across accounts: `OFR-<offer>_ANG-<angle>_FMT-<format>_SEG-<seg>_FUN-<TOF|BOF>_R<round>`. Add `utm_content={{ad.id}}` to URL tags. Log the mapping in the vault note.
- Review after 7 days; kill/scale rules tie to the account's breakeven (memory: reference_unit_economics). The testing engine plan lives in the vault: `Projects/creative-testing-engine.md`.

## Soumil's taste (learned, apply by default)
- Headline dominant, one focal point, plenty of empty space. He calls overfilled layouts "shabby". Fewer elements beat clever elements.
- Copy must be understood instantly. He rejected: comment threads, "Mine. Yours. Free.", "Shaadi season", a receipt with confusing maths. He liked: "One tube won't do it", "3 problems, pay for 2", clean receipts with a plain total, native and ugly formats, real people.
- Offer means the core promise, not a discount. Bottom-funnel offer ads must read as "pick ANY 3 from the range", not a fixed pack.
- Clay/diorama styles and generic brand-DNA template output are rejected. Use the arcads-style templates and real-people photography.
- No made-up claims, stats, testimonials, or label text.

## References
- `references/research-playbook.md` Meta queries, Amazon, Reddit, Ad Library, parsing code.
- `references/psychology-framework.md` vocabulary, offer/angle types, awareness levels, concept sheet format.
- `references/copy-principles.md` principles table, labelling template, critique checklist.
- `references/design-rules.md` hard rules. `references/design-systems.md` the systems with evidence.
- `references/funnel-playbook.md` TOF vs BOF.
- `references/chatgpt-pipeline.md` generation and download procedure with the gotchas.
- `references/qa-gate.md` 10-point gate and known failure modes.
- Older: `arcads-prompt-library.md` (37 templates), `safety-suffixes.md`, `gpt-image-guide.md`, `ad-clone-guide.md`, `example-mufasa-prompts.py`.
- `scripts/`: `reddit_research.py`, `chatgpt_helper.ps1`, `build_reference.py`, `contact_sheet.py`, `prompts_template.py`.

## Step 9: Launching in Meta (only when asked)
- Show all creatives in chat first and wait for approval.
- Upload images to the ad account via Dropbox (not the LOCAL_FILE widget).
- Build campaign (CBO), one ad set, one ad per creative; ask before activating.
