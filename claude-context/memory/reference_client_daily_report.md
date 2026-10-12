---
name: reference-client-daily-report
description: "How Soumil's WhatsApp client daily reports are built and sent (format, data sources, group chat ids, Meta account ids); used 5 Oct and 12 Oct 2026 for Ashopi and Mufasa Man"
metadata:
  node_type: memory
  type: reference
---

**Format (his own, plain text, one message per client, one block per day, no commentary):**
`<Brand> daily report` / blank line / `Oct 10` / `Orders: 2` / `Revenue: 1.8k` / `Ad Spend: ₹4894` / `ROAS: 0.37` / blank line / next day. Revenue is Shopify total sales rounded to the nearest 100 and shown in thousands with one decimal; ad spend is Meta spend rounded to the rupee with the ₹ sign; ROAS is Shopify revenue divided by Meta spend (two decimals), not Meta's own ROAS.

**Data:** orders and revenue come from Salaj's Shopify app screenshots (Soumil has no Shopify access for Ashopi or Mufasa); he asks "send ss plz" in the Salaj DM. Ad spend from the official Meta connector (`ads_get_ad_entities`, level ad_account, time_increment 1, fields amount_spent, omni_purchase, omni_purchase_values, purchase_roas; verify fields with ads_get_field_context first). Accounts: Ashopi `108956382644350`, Mufasa Man `611633726787161`.

**Groups (marker-method ids):** Mufasa Man `ndTq159yXF--MLF3sIcZrw` (120363409387983969@g.us), Ashopi `BIg_iijTVu-aQT_0YMPC7Q` (120363407810749249@g.us), Habbits `zslEcJC5WWKYsMBspXj3fg`, Bagwani `77zC3X1SVdWEDHmFkkVgJg`. See [[whatsapp-api-read-only]]. Check the provider id inside the send command, send with `-F "text=<file"` from a UTF-8 file (the ₹ sign breaks in a PowerShell argument), one approval click, pace 10 seconds between groups, verify by reading the newest message.

**History:** first reports 5 Oct (Oct 3 and 4); Oct 5 to 7 posted 7 and 8 Oct; on 12 Oct Salaj asked "Updates dedo ek baar sabme" and "Saturday and sunday both", Soumil said send Ashopi and Mufasa first and share Bagwani and Habbits himself. Oct 8 and 9 were never posted in the Ashopi and Mufasa groups. Mufasa Shopify equals Meta exactly; Ashopi Oct 10 differed (Shopify 2 orders Rs 1,831, Meta 1 purchase Rs 932), the Shopify figure was used. Never name another agency in a client message.

**Bagwani (12 Oct):** posted Oct 10 and 11 from his own Shopify desktop screenshots (Home page, date picker set to the day; Shopify shows "19K" or "19.7K", so revenue is accurate to about 100) and Meta account `1682300005612270` ("Bagwani by Neetu Khanna"): Oct 10 22 orders, 19.0k, Rs 9294, ROAS 2.0; Oct 11 22 orders, 19.7k, Rs 10289, ROAS 1.9. Bagwani reports use ROAS with ONE decimal (earlier ones: 1.9, 2.1, 1.7, 2.5) while Ashopi and Mufasa use two. Shopify and Meta differ here (Oct 11: Shopify 22 orders, Meta 18 purchases), store figure used. A Bagwani client asked on 8 Oct "Haven't received ad spent reports for last 2 days", so these reports matter to them.

**Ashopi Oct 8 and 9 (12 Oct 17:25):** the client asked in the group "Pls share for 8th n 9th too". Shopify screenshots (his own, desktop Home page): Oct 8 showed total sales -18.2k with 3 orders because the client cancelled many COD and out-of-stock orders that day (net sales go negative), Oct 9 showed 10K and 4 orders. Posted Oct 8 as 3 orders, revenue 3.1k (Meta value of that day's 3 orders, count matches Shopify), spend 4419, ROAS 0.70, plus a neutral one-line note that Shopify shows -18.2k net for Oct 8 because of the cancellations; Oct 9 as 4 orders, 10.0k, 4791, ROAS 2.09. Rule I used: when Shopify net sales for a day is distorted by cancellations, report the day's new-order value from Meta, say so in one neutral line, and tell Soumil. Message id IQdM3qJvWMui3LCvvqsj1Q. Ashopi is now reported Oct 3 to 11 with no gaps.

**Edit worked (12 Oct 17:26):** at his word ("remove the last note in ashopi") the note line was removed from the sent Ashopi Oct 8 and 9 report by editing the message in place: `PATCH /api/v1/messages/<message_id>` with a JSON body `{"text": ...}` (ASCII-escaped JSON file, `--data-binary @file`, Content-Type application/json) returned MessagePatched within WhatsApp's 15 minute edit window. The guard prompts once. Later he chose to leave Oct 8 as the clean numbers only, so for Oct 8 the group now shows 3.1k with no explanation of the -18.2k Shopify net figure.

