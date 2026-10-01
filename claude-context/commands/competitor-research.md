# Competitor Research

Run a full competitor map for a client. Input format:
`/competitor-research [Client name] — [product description], [price point], [geography], [target customer]`

Example: `/competitor-research Moiras — daily tiffin subscription, ₹299/day, Lower Parel/Worli/Dadar Mumbai, working professionals`

---

## Instructions

You are running a complete competitor research process for $ARGUMENTS. Extract from the input: (1) product/category, (2) price point, (3) geography, (4) target customer. If any are missing, ask before proceeding.

**Critical rule:** Never assume the client's vocabulary = competitors' vocabulary. A tiffin brand's competitors may call themselves "meal subscription," "diet delivery," or "cloud kitchen." A shoe brand's competitors may call themselves "footwear," "sneakers," or "kicks." Always research adjacent category terms, not just the client's own words.

Run all 7 steps. Do not skip any. Do not declare the map complete until all 7 are done.

---

### Step 1 — Listicles

Web search: `"best [category] in [city]"` across LBB, Magicpin, Lytmeals, JustDial, Sulekha, and any category-specific directories. Pull every brand name mentioned. This gets 60–70% of known brands — not sufficient alone.

### Step 2 — Customer discovery search

Ask: "Where does a customer in this market actually go when they want to find this product?" Search there. Do not assume a platform. For some categories it's Amazon, for some it's a marketplace, for some it's Google Maps, for some there is no platform (D2C-only). Figure it out from the product and geography, then search.

### Step 3 — Hyper-local Google search

Search `"[product/category] [specific neighbourhood/zone]"` — not just city-level. Brands invisible at city level often appear in neighbourhood-level searches. Run this for each of the client's key delivery/service zones.

### Step 4 — Instagram hashtag search

Web search for Instagram hashtags: `#[city][category]`, `#[category][city]`, `#[city]food`, `#[neighbourhood]` variations. Some competitors have no website, no listicle presence, no paid ads — Instagram is their only footprint. This is the only way to find them. True Tiffins (Mumbai) was only discoverable this way.

### Step 5 — Meta Ads Library sweep

Use the ScrapeCreators API to pull live paid ads data. API key: `OasSS0zklCOvB2317jK1vozG3qV2`

Run at minimum 8 keyword queries — covering the client's category name AND adjacent categories:

```powershell
$headers = @{'x-api-key'='OasSS0zklCOvB2317jK1vozG3qV2'}

$keywords = @(
    "[category keyword 1]",
    "[category keyword 2]",
    "[adjacent category term 1]",
    "[adjacent category term 2]",
    "[delivery mechanic or USP term]",
    "[geo + category]",
    "[target customer pain point]",
    "[competitor name if already known]"
)

foreach ($kw in $keywords) {
    $encoded = [System.Uri]::EscapeDataString($kw)
    $r = Invoke-RestMethod -Uri "https://api.scrapecreators.com/v1/facebook/adLibrary/search/ads?query=$encoded&country=IN&status=ACTIVE" -Headers $headers
    Write-Output "[$kw] → $($r.searchResults.Count) ads"
    foreach ($ad in $r.searchResults | Select-Object -First 3) {
        $copy = $ad.snapshot.body.text
        if ($copy.Length -gt 150) { $copy = $copy.Substring(0,150) }
        Write-Output "  Page: $($ad.snapshot.page_name) | CTA: $($ad.snapshot.cta_text) | Copy: $copy"
    }
}
```

For each brand found running paid ads: pull all unique ad copies, note active ad count, CTA, creative angles, and pricing if mentioned.

Note remaining ScrapeCreators credits after use. If credits are low (<20), flag it.

### Step 6 — Competitor cross-reference

For the top 5 competitors found, web search their Instagram/Facebook pages. Look at who they follow, who follows them, what accounts they tag. Competitors know each other. This surfaces brands that don't appear in any search but are known within the category.

### Step 7 — Website fetch for key competitors

For every competitor confirmed to be in the client's geography and price range, fetch their website. Extract: exact pricing, delivery zones, subscription model, key USPs, and creative/copy angle. Do not rely on search summaries — fetch the actual page.

---

## Output format

Deliver in four sections:

**Section A — Direct competitors** (same geography, same price range, same customer)
Table: Name | Price | Instagram followers | Delivery zones confirmed | Paid Meta ads (Y/N + count) | Key angle | Threat level

**Section B — Paid Meta advertisers** (anyone running ads in this category, regardless of geography)
Table: Advertiser | Active ads | CTA | Top creative angle | Threat

**Section C — Adjacent competitors** (different price point or positioning, but fishing same customer pool)
Table: Name | Price | Positioning | Why they matter

**Section D — Strategic findings**
- Who is the real paid competition?
- What angles are uncontested in paid ads?
- What is the client's strongest differentiator that no competitor is using?
- What is the actual status quo competitor (the thing prospects do instead of buying from the client)?

---

## After completing research

Save the output to the vault at `C:\Users\soumi\Documents\Vault\Projects\[client-name]-competitor-map.md` using the appropriate template. Ask before saving if the file already exists.

If you find a gap in this skill mid-research (a step that didn't work or a platform that should have been included), flag it explicitly and ask if the skill file should be updated before continuing.
