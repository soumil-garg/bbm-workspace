---
name: project-lotus-tracking-fix
description: "Lotus Meta product-code fix status (11 Oct 2026): bridge script live in Miva Global Footer, two auto rules off, Purchase (INVC) script still to replace"
metadata:
  node_type: memory
  type: project
  originSessionId: a739310d-7f94-4cb8-bf86-da81ce406b3c
  modified: 2026-10-11T17:54:47.060Z
---

Kyle approved the product code fix. State on 2026-10-11:
- Bridge script is live in the Miva Global Footer (pasted by Soumil by hand; the auto-mode classifier blocks programmatic writes into the live Miva editor, so hand-paste handoff is the route). Source and undo in vault note lotus-sculpture-tracking-diagnosis-oct2026 (status log). ViewContent and InitiateCheckout verified live with content_ids; AddToCart path ran.
- Event Setup Tool rules AddToCart 1314328459972615 and InitiateCheckout 1447585525922341 switched INACTIVE on 11 Oct (undo = ACTIVE via ads_pixel_event_update). Purchase rule 441177122122094 INACTIVE since 7 Oct.
- Still open: replace INVC Purchase Script A (once per order, event_id = order id, product codes), delete broken Script B, coupon test order (code 100), check catalog match rate after 24 to 48 hours.

**Why:** catalog match rate was 0% because Meta events carried no content_ids.
**How to apply:** Public site is behind a Cloudflare challenge for the built-in browser; verify via the Brave tab (Claude in Chrome, Browser 1), open a NEW tab and never navigate his admin tab. Brave Shields block the pixel beacon, so read `fbq.queue` instead of network requests. Related: [[client_lotus_sculpture]], [[reference_miva_api_client]].
