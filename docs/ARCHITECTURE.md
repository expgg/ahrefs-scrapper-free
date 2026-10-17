# Architecture & Engine Overview

**Ahrefs Auto Scraper v3.5** is an autonomous click-automator, multi-seed crawler, and SEO intelligence engine built for high-throughput keyword research without requiring paid API subscriptions.

---

## 1. Stealth Core & Anti-Bot Bypass

* **SeleniumBase UC Mode (Undetected ChromeDriver):** Patches low-level Chrome DevTools Protocol (`Runtime.enable`, `Page.addScriptToEvaluateOnNewDocument`) fingerprints to prevent headless/automated browser detection.
* **Persistent Session Profile (`./chrome_profile`):** Preserves `cf_clearance` cookies, TLS fingerprints, and localStorage across runs, dramatically reducing Cloudflare Turnstile challenges.
* **Cloudflare Turnstile Handler:** Automatically identifies Turnstile challenges, executes native GUI clicks, solves the verification checkbox, and extracts session clearance tokens to `cf_session_token.json`.
* **Humanized Typing & Bezier Curves:** Types search seeds character-by-character with randomized intervals (`30ms - 80ms`) and variable delays mimicking human keystrokes.

---

## 2. On-Screen Virtual Cursor & Idle Wanderer

* **Visual Neon Pointer:** An in-browser glowing cursor (`#00E5FF`) rendered over the DOM with smooth CSS transitions, glowing trails, and click ripple effects.
* **5-Second Idle Wanderer:** If the scraper enters an inspection sleep or waits for DOM rendering for > 5 seconds, the cursor wakes up and wanders across result rows, applying reading hover states (`rgba(0, 229, 255, 0.15)`).
* **Modal Table Scroll Engine:** Dynamically locates the inner scroll container (`.ReactModalPortal div[class*='content']`) and dispatches smooth wheel scrolls, ensuring rows render into view for screen recording or live viewing.

---

## 3. Balanced Seed Diversity & Anti-Monopoly Priority Heap

To prevent recursive keyword generation from getting stuck in single-brand loops (e.g. 50 Sony-only queries):
* **Max-Priority Heap:** Seeds are scored based on search volume tier, KD accessibility, and topic frequency.
* **Topic Frequency Penalty:** Subtopic words (e.g. `sony`, `apple`, `wireless`) incur a cumulative decay penalty each time they are queried, ensuring diverse parent branches (`noise cancelling`, `running`, `budget`, `gaming`) are explored.

---

## 4. 12-Column SEO Intelligence Classification

Each scraped keyword is enriched into a structured 12-column intelligence schema:

| Column | Name | Purpose |
| :---: | :--- | :--- |
| **#** | Rank | Ordered position ranked by AI Opportunity Score. |
| **Target Keyword** | Keyword String | Cleaned query extracted from Phrase Match or Questions tab. |
| **Opp Score** | Opportunity Score (1–100) | Composite rating factoring volume, KD tier, intent, and word count. |
| **Exact KD** | Exact 0–100 KD | Verified numeric difficulty scraped from Ahrefs KD Tool. |
| **KD Tier** | Accessibility Tier | Easy, Medium, Hard, or Super Hard. |
| **Search Volume** | Monthly Search Volume | Estimated search volume (`>10k`, `>1k`, etc.). |
| **Search Intent** | User Intent | Informational, Commercial, Transactional, or General. |
| **Backlinks Needed** | Link Requirement | Estimated referring domains needed to rank in Top 10. |
| **Keyword Tail** | Length Tier | Short-tail (<=2 words), Mid-tail (3 words), or Long-tail (4+ words). |
| **Word Count** | Length | Integer word count. |
| **Topic Cluster** | Parent Seed | Seed query that generated this keyword. |
| **Match Type** | Source Tab | Phrase Match or Questions. |

---

## 5. Google Apps Script Live WebSocket Synchronization

* **Zero-Setup Automation:** Python issues HTTP POST payloads to a deployed Google Apps Script Web App.
* **Standalone Sheet Creation:** If no `sheet_id` is supplied, Apps Script executes `SpreadsheetApp.create()` directly in Google Drive, naming it after the target seed.
* **Live Formulas & Badges:** Row 1 title banner, Row 2 KPI scorecard formulas, Row 3 frozen obsidian header, and conditional formatting rules are constructed programmatically.
* **Stage 2 Badge Illumination:** Individual keyword KD scores and backlink metrics update row-by-row in real time via Google's cloud WebSockets.
