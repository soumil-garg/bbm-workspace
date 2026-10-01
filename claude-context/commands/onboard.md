# Client Onboarding

Run a complete client onboarding for a new brand. This covers brand verification, competitor research, and brief generation.

Input format:
`/onboard` followed by the filled client onboarding questionnaire (template at `C:\Users\soumi\Documents\Vault\Templates\client-onboarding-questionnaire.md`), or paste raw notes, WhatsApp messages, call notes — whatever you have. Claude will parse it.

The more complete the input, the faster and more accurate the onboarding. If critical fields are missing (ad account ID, campaign goal, geography), Claude will ask before proceeding.

---

## Instructions

You are onboarding a new client for Big Bigger Media. Parse $ARGUMENTS to extract every piece of information provided about the brand. Then execute all three parts below in order. Do not skip steps. Do not present partial information as complete.

If you find a gap in this skill mid-execution, flag it and ask if the skill file should be updated before continuing.

---

## Part 1 — Brand Verification

Verify every claim the client made about themselves. Do not trust what the client said — confirm it from primary sources.

**1a. Website**
Fetch their website. Extract: exact pricing, product description, delivery areas, subscription model, order channel, any USPs or claims. Flag any discrepancy between what the client told you and what the website says.

**1b. Instagram**
Web search `[brand name] instagram [city]` and fetch the profile page. Extract: follower count, following count, bio, number of posts, what their content looks like, engagement signals. If the handle was provided, use it directly.

**1c. Facebook**
Web search `[brand name] facebook [city]`. Fetch the page. Extract: likes, follows, bio, how active they are, any pinned posts visible.

**1d. Their own Meta ads — via Ads Library**
Pull their own live ads using ScrapeCreators API. API key: `OasSS0zklCOvB2317jK1vozG3qV2`

```powershell
$headers = @{'x-api-key'='OasSS0zklCOvB2317jK1vozG3qV2'}
$brandName = "[brand name or page name]"
$encoded = [System.Uri]::EscapeDataString($brandName)
$r = Invoke-RestMethod -Uri "https://api.scrapecreators.com/v1/facebook/adLibrary/search/ads?query=$encoded&country=IN&status=ALL" -Headers $headers
Write-Output "Total ads found: $($r.searchResults.Count)"
foreach ($ad in $r.searchResults) {
    $copy = $ad.snapshot.body.text
    if ($copy.Length -gt 200) { $copy = $copy.Substring(0,200) }
    Write-Output "Active: $($ad.is_active) | Format: $($ad.snapshot.display_format) | CTA: $($ad.snapshot.cta_text) | Copy: $copy"
    Write-Output "---"
}
```

Note: how many ads are live, what the actual ad copy says, what formats they're using, what CTAs. Compare against what the client told you.

**1e. Ad account data** (if ad account ID was provided)
Use the Meta Ads MCP (mcp__9c1ec85d) to pull campaign-level and ad-level insights for the last 30 days. Extract: spend, key metric (ROAS/CPL/CPP), CTR, what's running, what's paused. This is ground truth — use it to validate any performance claims the client made.

**1f. Verification summary**
After completing 1a–1e, state:
- What the client told you vs. what you verified
- Any discrepancies (pricing, delivery areas, ad count, performance claims)
- Gaps where you could not verify (and why)

---

## Part 2 — Competitor Research

Run the full 7-step competitor research process. Do not shortcut this.

**Critical rule:** Never assume the client's vocabulary = competitors' vocabulary. Always research adjacent category terms, not just the client's own words.

### Step 1 — Listicles
Web search: `"best [category] in [city]"` across LBB, Magicpin, Lytmeals, JustDial, Sulekha, and any category-specific directories. Pull every brand name mentioned.

### Step 2 — Customer discovery search
Ask: "Where does a customer in this market actually go when they want to find this product?" Search there. Do not assume a platform. Figure it out from the product and geography per client — do not hardcode a platform.

### Step 3 — Hyper-local Google search
Search `"[category] [specific neighbourhood/zone]"` for each of the client's key delivery/service zones — not just city-level.

### Step 4 — Instagram hashtag search
Web search for Instagram hashtags: `#[city][category]`, `#[category][city]`, `#[neighbourhood]` variations. Some competitors exist only on Instagram with no website, no listicle, no paid ads.

### Step 5 — Meta Ads Library sweep
Run minimum 8 keyword queries covering the client's category AND adjacent categories. Use the same ScrapeCreators API call pattern from Part 1 above, cycling through keywords:
- Category name (exact)
- Adjacent category terms (what competitors might call the same product)
- Delivery mechanic or key USP terms
- Geo + category combinations
- Target customer pain point terms
- Any competitor names already found

For each brand found running paid ads: pull all unique ad copies, note active ad count, CTA, creative angles, pricing if mentioned.

Note remaining ScrapeCreators credits after use. If credits drop below 20, flag it.

### Step 6 — Competitor cross-reference
For the top 5 competitors found, look at who they follow and who follows them on Instagram. Competitors know each other. This surfaces brands invisible to search.

### Step 7 — Website fetch for key competitors
Fetch the website of every confirmed in-geography, in-price-range competitor. Extract: exact pricing, delivery zones, subscription model, key USPs, copy angles. Do not rely on search summaries.

---

## Part 3 — Brief Generation

Compile everything into a structured onboarding brief and save it to the vault.

Save to: `C:\Users\soumi\Documents\Vault\Projects\[client-name]-onboarding-brief.md`

Brief structure:

```
# [Client Name] — Client Onboarding Brief

*Researched: [date]. Sources: [list every source used]*

## 1. What They Actually Sell
(verified product, price, model, delivery, order channel, conversion path)

## 2. Who the Real Buyer Is
(verified audience — who is actually buying, not who the client thinks is buying)

## 3. Verification Findings
(what the client told us vs. what primary sources confirmed — every discrepancy flagged)

## 4. Competitor Landscape
### 4a. Direct competitors (same geo, same price, same customer)
### 4b. Paid Meta advertisers (anyone running ads in this category)
### 4c. Adjacent competitors (different positioning, same customer pool)
### 4d. Key strategic findings

## 5. Current Creative Audit
(all live ads: angle, hook, format, verdict)

## 6. What's Missing / Untested Angles
(gaps in current creative based on competitor intelligence)

## 7. Recommendations
(immediate actions before new creatives, testing protocol)
```

After saving, confirm the file path and give a 5-line executive summary of the most important findings.

---

## Updating this skill

If any step fails, a platform is blocked, or a better method is discovered mid-execution — flag it explicitly and ask if the skill file should be updated before continuing. This skill should improve every time it runs.
