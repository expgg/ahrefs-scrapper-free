<div align="center">

# ⚡ Ahrefs Auto Scraper v3.5
### *Autonomous Keyword Harvester & SEO Intelligence Engine*

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SeleniumBase](https://img.shields.io/badge/SeleniumBase-UC%20Mode-FF6F00?style=for-the-badge&logo=selenium&logoColor=white)](https://github.com/seleniumbase/SeleniumBase)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-Live%20Streaming-34A853?style=for-the-badge&logo=googlesheets&logoColor=white)](https://workspace.google.com/)
[![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=for-the-badge)]()

**Automate Ahrefs Free Keyword Generator & Keyword Difficulty without API subscriptions.**  
*Harvest thousands of high-opportunity keywords, scrape exact 0–100 KD scores with backlink estimates, and stream them live into auto-generated executive Google Sheets dashboards.*

---

[Quick Start](#-quick-start) • [Key Features](#-features) • [Google Sheets Setup](docs/GOOGLE_SHEETS_SETUP.md) • [Architecture](docs/ARCHITECTURE.md) • [Sample Data](samples/sample_keyword_intelligence.csv)

---

</div>

## 📌 Overview

**Ahrefs Auto Scraper** is a production-ready, stealth click-automator and SEO intelligence suite. By orchestrating [Ahrefs Free Keyword Generator](https://ahrefs.com/keyword-generator) and [Ahrefs Keyword Difficulty Tool](https://ahrefs.com/keyword-difficulty) with an undetectable Chrome profile and anti-bot mitigation, it extracts hundreds of keywords, scores their search viability, and exports them directly into CSV and real-time cloud dashboards.

### 🌟 Why This Exists:
* **No $99/mo Ahrefs Plan Required:** Tap into public keyword data and difficulty scores 100% free.
* **1-Click Google Drive Dashboard:** Spins up a brand-new, standalone Google Sheet for every run with KPI cards and obsidian headers.
* **Stealth Turnstile Bypass:** Persistent session profile caches `cf_clearance` tokens to bypass Cloudflare verification seamlessly.
* **Smart Seed Diversity:** Prevents brand monopoly rabbit holes with an automated priority decay algorithm.

---

## ⚡ Quick Start

### Option A: 1-Click Launch (Windows)
1. **First-time setup:** Double-click [`INSTALL_DEPENDENCIES.bat`](INSTALL_DEPENDENCIES.bat) to install requirements.
2. **Launch:** Double-click [`LAUNCH_SCRAPER.bat`](LAUNCH_SCRAPER.bat) to run the interactive scraper.

*(The launcher auto-verifies dependencies on every launch and installs any missing packages automatically).*

### Option B: Terminal (CLI)
```bash
# 1. Clone the repository
git clone https://github.com/expgg/ahrefs-scrapper-free.git
cd ahrefs-scrapper-free

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch interactive prompt
python keyword_automator.py
```

### Option C: Direct Command Line Flags
```bash
# Target 100 keywords in the UK with exact KD lookup on top 10 winners
python keyword_automator.py --seed "wireless headphones" --quota 100 --country "United Kingdom" --enrich-kd 10

# Multi-seed search across multiple branches
python keyword_automator.py --seed "smart watch, fitness band, running watch" --quota 150 --enrich-all
```

---

## 🚀 Features

### 📊 1. Standalone Google Sheet Per Research Session
Every research session automatically spins up a brand-new, independent Google Sheet on your Google Drive:
* **Row 1:** Electric Cyan `#00E5FF` Title Banner showing topic and timestamp.
* **Row 2:** 4 Live Executive KPI Scorecards (*Total Harvested*, *Average Opp Score*, *Zero-Backlink Gems*, *Commercial Buyer Intent %*).
* **Row 3:** Sticky frozen Obsidian header (`#0B0F19`) with frozen panes and auto-filter.
* **Row 4+:** High-contrast data badges that stream in live as keywords are harvested.
* **Real-Time Stage 2 Illumination:** As Ahrefs investigates each winner in the KD tool, row cells light up individually with exact KD and backlink requirements.

> *For a 2-minute setup guide on linking your Google Account, read the [Google Sheets Setup Guide](docs/GOOGLE_SHEETS_SETUP.md).*

---

### 🖱️ 2. On-Screen Virtual Cursor & 5-Second Idle Wanderer
* **Visual Glow Pointer:** Renders an animated `#00E5FF` virtual pointer over Chrome with smooth transitions and click ripple effects.
* **Idle Mouse Wanderer:** If the browser waits or idles for > 5 seconds, the cursor gently wanders across rows, highlighting cells with reading hover effects for maximum humanization and visual flair.
* **True Modal Table Scrolling:** Dynamically targets inner modal containers (`.ReactModalPortal div[class*='content']`) rather than the background window.

---

### 🎯 3. Bulletproof Country Selection
* Targets over 100+ countries with keyboard combobox search and physical enter dispatch.
* Triggers an emerald-green visual confirmation flash on the country badge once confirmed.

---

### 🧠 4. Balanced Seed Priority Engine
* Uses a min/max priority heap to continuously explore fresh search branches.
* Automatically penalizes overused subtopics (e.g., `sony`, `apple`, `wireless`) with a decay multiplier, ensuring your quota captures long-tail gems across diverse categories.

---

### 📈 5. 12-Column SEO Intelligence Architecture

Every exported CSV and Google Sheet is structured with 12 standardized columns:

| Column | Header | Type | Description |
| :---: | :--- | :---: | :--- |
| `1` | **#** | Integer | Rank ordered by AI Opportunity Score. |
| `2` | **Target Keyword** | String | The harvested keyword query. |
| `3` | **Opp Score** | 1–100 | Composite viability score (Volume + Low KD + Intent + Length). |
| `4` | **Exact KD** | 0–100 | Verified numeric difficulty scraped from Ahrefs KD Tool. |
| `5` | **KD Tier** | String | Easy (0–29), Medium (30–69), Hard (70–84), Super Hard (85–100). |
| `6` | **Search Volume** | String | Monthly search volume tier (`>100k`, `>10k`, `>1k`, etc.). |
| `7` | **Search Intent** | String | Commercial, Transactional, Informational, or General. |
| `8` | **Backlinks Needed** | String | Estimated referring domains needed for Top 10 rankings (`~0 websites` = Goldmine). |
| `9` | **Keyword Tail** | String | Short-tail (<=2 words), Mid-tail (3 words), Long-tail (4+ words). |
| `10` | **Word Count** | Integer | Number of words in the query. |
| `11` | **Topic Cluster** | String | Parent seed keyword that originated this branch. |
| `12` | **Match Type** | String | Source tab (`Phrase Match` or `Questions`). |

*(Inspect a live export in [`samples/sample_keyword_intelligence.csv`](samples/sample_keyword_intelligence.csv)).*

---

## ⚙️ CLI Flags & Parameters

| Flag | Long Flag | Default | Description |
| :--- | :--- | :---: | :--- |
| `-s` | `--seed` | Prompt | Primary seed keyword(s), comma-separated. |
| `-q` | `--quota` | `50` | Total target unique keywords to harvest. |
| `-c` | `--country` | `United States` | Target country (e.g. `United Kingdom`, `Canada`, `Germany`). |
| | `--enrich-kd` | `10` | Number of top candidates to look up exact 0–100 KD for (`0` to skip). |
| | `--enrich-all` | `False` | Scrapes exact KD and backlinks for ALL harvested keywords. |
| | `--sheet-url` | `Config` | Google Apps Script Webhook URL for live streaming. |
| `-o` | `--output` | Auto | Custom CSV output filename. |
| | `--no-questions` | `False` | Exclude scraping from the Questions tab. |

---

## 📂 Project Structure

```
ahrefs-scrapper-free/
│
├── config/
│   └── sheet_config.example.json   # Template configuration for Google Sheets Webhook
│
├── docs/
│   ├── ARCHITECTURE.md             # Technical deep-dive on stealth automation & scoring
│   └── GOOGLE_SHEETS_SETUP.md      # Step-by-step Google Apps Script setup guide
│
├── google_sheets/
│   └── code.gs                     # Google Apps Script engine for Drive auto-creation
│
├── samples/
│   └── sample_keyword_intelligence.csv # Clean 12-column sample dataset
│
├── .gitignore                      # Security rules (excludes browser cookies & personal tokens)
├── INSTALL_DEPENDENCIES.bat        # 1-click Windows dependency installer
├── LAUNCH_SCRAPER.bat              # 1-click Windows master launcher
├── LICENSE                         # MIT License
├── README.md                       # Master documentation & visual guide
├── requirements.txt                # Pinned Python package dependencies
└── keyword_automator.py            # Main automation engine & CLI HUD
```

---

## 🛡️ Anti-Bot & Cloudflare Notice

This tool uses **SeleniumBase Undetected ChromeDriver (UC Mode)**. On your very first run, Cloudflare Turnstile may display a *"Verify you are human"* checkbox. 
* Simply click the checkbox once manually in Chrome.
* The script immediately captures your `cf_clearance` token and stores it in `./chrome_profile`.
* Subsequent runs will load your authenticated session and bypass Turnstile automatically!

---

## 👤 Author & Credits

**Engineered by:** Al Hossain Rifat  
* **GitHub:** [@expgg](https://github.com/expgg)  
* **Repository:** [ahrefs-scrapper-free](https://github.com/expgg/ahrefs-scrapper-free)

*Disclaimer: This project is an independent automation tool developed for educational, data analysis, and SEO research purposes. It is not affiliated with, endorsed by, or associated with Ahrefs Pte. Ltd.*

---

<div align="center">
⭐ If you found this useful, star the repo on GitHub! ⭐
</div>
