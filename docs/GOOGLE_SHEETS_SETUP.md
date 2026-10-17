# Dedicated Google Sheets Per Research Engine (Cyber Dashboard Edition)

Transform your keyword research into automated, dedicated **SEO Intelligence Dashboards** generated directly inside your Google Drive.

### Features
* **Zero Manual Setup:** You never have to manually create sheets or paste sheet IDs again.
* **1 New Sheet Per Run:** Every keyword research project automatically spins up a brand-new, standalone Google Sheet on your Google Drive named `[SEED] - SEO Keyword Intelligence ([DATE])`.
* **Row 1 Executive Title Banner:** Deep obsidian `#050811` background with `#00E5FF` electric cyan typography.
* **Row 2 Live Calculating KPI Cards:** Real-time summary formulas (`Total Harvested`, `Average Opp Score`, `Zero-Backlink Gems`, `Commercial Buyer Intent %`).
* **Row 3 Sticky Obsidian Header:** `#0B0F19` background with `#00E5FF` electric cyan text, auto-filters, frozen panes, and explicit pixel column widths.
* **Cyber High-Contrast Badges:** Color-coded badges for Opportunity Score, Exact KD, Search Intent, Search Volume, and zero-backlink easy wins.
* **Real-Time Badge Illumination:** Watch individual cells update in real time as Stage 2 audits exact KD and backlinks.
* **Clickable Link in Terminal:** When complete, the CLI prints the direct link to your newly generated Google Sheet.

---

### Step 1: Deploy Apps Script (1 Minute)
1. Open [script.google.com](https://script.google.com/) and create a new project (or in Google Sheets, click **Extensions** → **Apps Script**).
2. Copy the entire contents of [`google_sheets/code.gs`](../google_sheets/code.gs) and paste it into `Code.gs`.
3. Click the **Save** icon (`Ctrl + S`).

---

### Step 2: Deploy as Web App
1. Click the blue **Deploy** button (top right) → **New deployment** (or **Manage deployments** if updating).
2. Click the gear icon ⚙️ next to "Select type" → choose **Web app**.
3. Set:
   * **Execute as:** `Me`
   * **Who has access:** `Anyone` (allows your local Python automator to stream data without OAuth credentials).
4. Click **Deploy**.
5. Authorize access if prompted by Google.
6. Copy the **Web app URL** (e.g. `https://script.google.com/macros/s/.../exec`).

---

### Step 3: Configure Your Local Webhook
Save your Web App URL into `sheet_config.json` in the project root:

```json
{
  "sheet_url": "https://script.google.com/macros/s/YOUR_DEPLOYED_WEB_APP_ID/exec"
}
```

*(You can also use `config/sheet_config.example.json` as a starting template).*

---

### Step 4: Run the Scraper
Run the engine via the 1-click batch launcher or terminal:

```powershell
# Interactive mode (will auto-detect your saved sheet_config.json):
python keyword_automator.py

# Or pass directly via CLI flag:
python keyword_automator.py --seed "wireless headphones" --quota 50 --country "United Kingdom" --enrich-kd 10
```

The script will automatically create the sheet, stream rows live, and display the direct link upon completion!
