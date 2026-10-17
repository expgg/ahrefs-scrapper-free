"""
=============================================================================
                           Ahrefs Auto Scraper
                        Made by Al Hossain Rifat
=============================================================================
Features:
  1. Virtual On-Screen Neon Cursor: Glowing cursor moves, hovers, and pulses with
     click ripples directly in the browser so you can watch it live.
  2. True Table Scrolling: Scrolls the actual keyword table rows smoothly into view.
  3. Bulletproof Country Selection: Accurate dropdown search & physical click.
  4. Multi-Seed Support: Input multiple comma-separated seeds.
  5. Balanced Seed Diversity: Anti-monopoly cooldown prevents single-brand rabbit holes.
  6. Full SEO Intelligence: Search Intent, Keyword Tail, Word Count & Opportunity Score (1-100).
  7. Exact Numeric KD Lookup: Scrapes real 0-100 KD & Backlinks on top candidates or 'all'.
  8. Live Google Sheets Webhook: Real-time streaming into Google Sheets.
=============================================================================
"""

import sys
import os
import io
import time
import re
import random
import heapq
import argparse
from datetime import datetime
import pandas as pd
import requests

# Force UTF-8 on Windows terminal to prevent cp1252 encoding crashes
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        try:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass

from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# Rich console styling
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import box
    console = Console(file=sys.stdout, legacy_windows=False, force_terminal=True, safe_box=True)
    HAS_RICH = True
except ImportError:
    HAS_RICH = False
    console = None


def print_banner():
    if HAS_RICH:
        console.print()
        console.print("[bold cyan]✦ Ahrefs Auto Scraper[/bold cyan] [dim]v3.5[/dim]")
        console.print("[dim]Autonomous Keyword Harvester & SEO Intelligence Engine[/dim]")
        console.print("[italic yellow]Made by Al Hossain Rifat[/italic yellow]\n")
    else:
        print("\n* Ahrefs Auto Scraper v3.5")
        print("Autonomous Keyword Harvester & SEO Intelligence Engine")
        print("Made by Al Hossain Rifat\n")


def print_config_panel(seed_keywords, quota, country, enrich_kd_display, sheet_url, output_path):
    if HAS_RICH:
        grid = Table.grid(expand=True, padding=(0, 2))
        grid.add_column(style="bold cyan", justify="left")
        grid.add_column(style="white", justify="left")
        grid.add_column(style="bold cyan", justify="left")
        grid.add_column(style="white", justify="left")

        grid.add_row("Seeds:", f"[yellow]{', '.join(seed_keywords)}[/yellow]", "Target Geo:", f"[green]{country}[/green]")
        grid.add_row("Quota:", f"[magenta]{quota} keywords[/magenta]", "KD Lookups:", f"[gold1]{enrich_kd_display}[/gold1]")
        webhook_status = "[green]Connected[/green]" if sheet_url else "[dim]Disabled (Local CSV)[/dim]"
        grid.add_row("Live Webhook:", webhook_status, "Output File:", f"[dim]{output_path}[/dim]")

        p = Panel(grid, title="[bold cyan] ACTIVE SESSION PARAMETERS [/bold cyan]", border_style="cyan", box=box.ROUNDED)
        console.print(p)
        console.print()
    else:
        print("-" * 65)
        print(f"Seeds: {', '.join(seed_keywords)} | Target Geo: {country}")
        print(f"Quota: {quota} keywords | KD Lookups: {enrich_kd_display}")
        print(f"Output File: {output_path}")
        print("-" * 65 + "\n")


# ---------------------------------------------------------------------------
# Visual Virtual Cursor & Human Animations ("WOW Factor")
# ---------------------------------------------------------------------------

INJECT_CURSOR_JS = """
if (!document.getElementById('virtual-bot-cursor')) {
    const cursor = document.createElement('div');
    cursor.id = 'virtual-bot-cursor';
    cursor.style.position = 'fixed';
    cursor.style.zIndex = '9999999';
    cursor.style.width = '18px';
    cursor.style.height = '18px';
    cursor.style.borderRadius = '50%';
    cursor.style.background = 'rgba(0, 229, 255, 0.9)';
    cursor.style.border = '2px solid #ffffff';
    cursor.style.boxShadow = '0 0 15px #00e5ff, 0 0 30px #00e5ff';
    cursor.style.pointerEvents = 'none';
    cursor.style.transform = 'translate(-50%, -50%)';
    cursor.style.transition = 'left 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), top 0.4s cubic-bezier(0.2, 0.8, 0.2, 1), transform 0.2s ease';
    cursor.style.top = '120px';
    cursor.style.left = '120px';
    document.body.appendChild(cursor);
    
    window.lastBotActivity = Date.now();
    
    window.botCursorMove = function(x, y) {
        window.lastBotActivity = Date.now();
        cursor.style.left = x + 'px';
        cursor.style.top = y + 'px';
    };
    
    window.botCursorClick = function(x, y) {
        window.lastBotActivity = Date.now();
        cursor.style.left = x + 'px';
        cursor.style.top = y + 'px';
        cursor.style.transform = 'translate(-50%, -50%) scale(0.6)';
        
        const ripple = document.createElement('div');
        ripple.style.position = 'fixed';
        ripple.style.zIndex = '9999998';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.style.width = '14px';
        ripple.style.height = '14px';
        ripple.style.borderRadius = '50%';
        ripple.style.border = '2px solid #00ff88';
        ripple.style.transform = 'translate(-50%, -50%) scale(1)';
        ripple.style.transition = 'all 0.5s ease-out';
        ripple.style.pointerEvents = 'none';
        document.body.appendChild(ripple);
        
        setTimeout(() => {
            ripple.style.transform = 'translate(-50%, -50%) scale(5)';
            ripple.style.opacity = '0';
        }, 20);
        setTimeout(() => { ripple.remove(); }, 600);
        setTimeout(() => { cursor.style.transform = 'translate(-50%, -50%) scale(1)'; }, 200);
    };

    // Idle Mouse Wanderer (activates smoothly if idle > 5 seconds)
    if (!window.idleWandererInterval) {
        window.idleWandererInterval = setInterval(() => {
            if (Date.now() - window.lastBotActivity >= 5000) {
                const candidates = document.querySelectorAll('table tr, [class*="chartValue"], [class*="badge"], button');
                if (candidates.length > 0) {
                    const el = candidates[Math.floor(Math.random() * Math.min(candidates.length, 15))];
                    const rect = el.getBoundingClientRect();
                    if (rect.top >= 0 && rect.bottom <= window.innerHeight && rect.width > 0) {
                        const targetX = rect.left + rect.width * (0.2 + Math.random() * 0.6);
                        const targetY = rect.top + rect.height * (0.2 + Math.random() * 0.6);
                        cursor.style.left = targetX + 'px';
                        cursor.style.top = targetY + 'px';
                        
                        // Subtle reading highlight
                        const origBg = el.style.backgroundColor;
                        el.style.transition = 'background-color 0.4s ease';
                        el.style.backgroundColor = 'rgba(0, 229, 255, 0.08)';
                        setTimeout(() => { el.style.backgroundColor = origBg; }, 1200);
                    }
                }
            }
        }, 3000);
    }
}
"""

def move_cursor_to(driver, element, click=False):
    """Smoothly moves the on-screen neon virtual cursor to element and animates a click ripple."""
    try:
        driver.execute_script(INJECT_CURSOR_JS)
        rect = driver.execute_script("const r = arguments[0].getBoundingClientRect(); return [r.left + r.width/2, r.top + r.height/2];", element)
        x, y = rect[0], rect[1]
        if click:
            driver.execute_script(f"window.botCursorClick({x}, {y});")
        else:
            driver.execute_script(f"window.botCursorMove({x}, {y});")
        time.sleep(0.35)
    except Exception:
        pass


def human_type_animated(driver, element, value: str):
    """Simulates realistic human typing with virtual cursor and glowing neon border."""
    move_cursor_to(driver, element, click=True)
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(0.2)

    driver.execute_script("""
        arguments[0].focus();
        arguments[0].style.transition = 'all 0.3s ease';
        arguments[0].style.boxShadow = '0 0 18px rgba(0, 229, 255, 0.9)';
        arguments[0].style.borderColor = '#00e5ff';
    """, element)
    time.sleep(0.2)

    element.send_keys(Keys.CONTROL + "a")
    element.send_keys(Keys.BACKSPACE)
    time.sleep(0.2)

    for char in value:
        element.send_keys(char)
        time.sleep(random.uniform(0.035, 0.075))

    time.sleep(0.2)
    driver.execute_script("arguments[0].style.boxShadow = ''; arguments[0].style.borderColor = '';", element)


def highlight_and_click(driver, element):
    """Pulsating glow animation + virtual cursor click."""
    move_cursor_to(driver, element, click=True)
    try:
        driver.execute_script("""
            arguments[0].style.transition = 'all 0.25s ease';
            arguments[0].style.transform = 'scale(1.04)';
            arguments[0].style.boxShadow = '0 0 20px #ff8d00';
        """, element)
        time.sleep(0.25)
        driver.execute_script("arguments[0].click();", element)
        time.sleep(0.15)
        driver.execute_script("arguments[0].style.transform = 'scale(1)'; arguments[0].style.boxShadow = '';", element)
    except Exception:
        driver.execute_script("arguments[0].click();", element)


def smooth_scroll_table(driver):
    """
    Smoothly scrolls the actual keyword results modal container (not the background page),
    then lets the virtual cursor hover across a couple of rows before smoothly returning to top.
    """
    try:
        driver.execute_script(INJECT_CURSOR_JS)
        scroll_res = driver.execute_script("""
            const table = document.querySelector('table');
            if (!table) return null;
            let container = null;
            let p = table;
            while (p && p !== document.body) {
                const st = window.getComputedStyle(p);
                if ((st.overflowY === 'auto' || st.overflowY === 'scroll') && p.scrollHeight > p.clientHeight) {
                    container = p;
                    break;
                }
                p = p.parentElement;
            }
            if (!container) {
                container = document.querySelector(".ReactModalPortal div[class*='content']");
            }
            if (!container) return null;
            
            container.scrollBy({ top: 380, behavior: 'smooth' });
            return { scrollHeight: container.scrollHeight, clientHeight: container.clientHeight };
        """)

        if scroll_res:
            time.sleep(1.0)
            rows = driver.find_elements(By.XPATH, "//table//tr")
            if len(rows) > 3:
                mid_idx = min(6, len(rows) - 1)
                move_cursor_to(driver, rows[mid_idx], click=False)
                time.sleep(0.6)

            # Scroll back up to the top of the table container
            driver.execute_script("""
                const table = document.querySelector('table');
                let p = table;
                while (p && p !== document.body) {
                    const st = window.getComputedStyle(p);
                    if ((st.overflowY === 'auto' || st.overflowY === 'scroll') && p.scrollHeight > p.clientHeight) {
                        p.scrollTo({ top: 0, behavior: 'smooth' });
                        return;
                    }
                    p = p.parentElement;
                }
                const c = document.querySelector(".ReactModalPortal div[class*='content']");
                if (c) c.scrollTo({ top: 0, behavior: 'smooth' });
            """)
            time.sleep(0.4)
    except Exception:
        pass


def handle_cookie_banner(driver):
    try:
        reject_btn = driver.find_elements(By.CSS_SELECTOR, ".cky-btn-reject, .cky-btn-accept")
        if reject_btn:
            driver.execute_script("arguments[0].click();", reject_btn[0])
            time.sleep(1)
    except Exception:
        pass


def is_turnstile_visible(driver):
    """Checks whether a Cloudflare Turnstile challenge widget or iframe is currently displayed."""
    try:
        selectors = [
            "iframe[src*='challenges.cloudflare.com']",
            "iframe[src*='cloudflare']",
            "iframe[src*='turnstile']",
            "iframe[title*='Cloudflare']",
            "div[id*='cf-turnstile']",
            "div[class*='cf-turnstile']",
            "div#turnstile-wrapper",
            "#challenge-stage",
            ".ray-id",
        ]
        for sel in selectors:
            elems = driver.find_elements(By.CSS_SELECTOR, sel)
            for el in elems:
                if el.is_displayed():
                    return True, el
        return False, None
    except Exception:
        return False, None


def extract_and_save_cf_token(driver):
    """Extracts the Cloudflare cf_clearance session cookie token and saves it to cf_session_token.json."""
    try:
        cookies = driver.get_cookies()
        token_info = {}
        for c in cookies:
            if c.get("name") in ["cf_clearance", "__cf_bm", "_cfuvid"]:
                token_info[c["name"]] = {
                    "value": c["value"],
                    "domain": c.get("domain", ""),
                    "path": c.get("path", "/"),
                    "expiry": c.get("expiry", None)
                }
        if "cf_clearance" in token_info:
            import json
            with open("cf_session_token.json", "w", encoding="utf-8") as f:
                json.dump(token_info, f, indent=2)
            return token_info["cf_clearance"]["value"]
    except Exception:
        pass
    return None


def wait_and_solve_turnstile(driver, max_wait=20):
    """
    Actively monitors for Cloudflare Turnstile verification challenge.
    Attempts auto-click using SeleniumBase UC mode, visual cursor guidance,
    and captures the cf_clearance access token.
    """
    has_cf = False
    for _ in range(4):
        visible, el = is_turnstile_visible(driver)
        if visible:
            has_cf = True
            break
        time.sleep(0.6)

    if not has_cf:
        return True

    if HAS_RICH:
        console.print("[bold yellow]  [!] Cloudflare verification challenge detected![/bold yellow]")
        console.print("[dim]      Attempting automated click on 'Verify you are human' box...[/dim]")
    else:
        print("  [!] Cloudflare verification challenge detected!")
        print("      Attempting automated click on 'Verify you are human' box...")

    # 1. Visual cursor guide to Turnstile frame
    try:
        _, el = is_turnstile_visible(driver)
        if el:
            move_cursor_to(driver, el, click=False)
    except Exception:
        pass

    # 2. Use SeleniumBase built-in Cloudflare Turnstile handlers
    try:
        driver.uc_gui_handle_cf()
        time.sleep(2)
    except Exception:
        try:
            driver.uc_gui_click_cf()
            time.sleep(2)
        except Exception:
            pass

    # 3. Check if solved or countdown
    solved = False
    for remaining in range(max_wait, 0, -1):
        visible, _ = is_turnstile_visible(driver)
        if not visible:
            solved = True
            break
        if remaining % 5 == 0:
            if HAS_RICH:
                console.print(f"[bold red]  [!] Please click the 'Verify you are human' checkbox in Chrome if still prompted ({remaining}s remaining)...[/bold red]")
            else:
                print(f"  [!] Please click the 'Verify you are human' checkbox in Chrome ({remaining}s remaining)...")
        time.sleep(1)

    # 4. Capture cf_clearance access token
    token = extract_and_save_cf_token(driver)
    if token:
        token_display = token[:10] + "..." + token[-6:]
        if HAS_RICH:
            console.print(f"[bold green]  [✓] Cloudflare verification cleared![/bold green] [dim]Token: {token_display} (saved to cf_session_token.json)[/dim]\n")
        else:
            print(f"  [✓] Cloudflare verification cleared! Token: {token_display} (saved to cf_session_token.json)\n")
    elif solved:
        if HAS_RICH:
            console.print("[bold green]  [✓] Cloudflare verification cleared![/bold green]\n")
        else:
            print("  [✓] Cloudflare verification cleared!\n")

    return solved


# ---------------------------------------------------------------------------
# Bulletproof Country Selection Engine
# ---------------------------------------------------------------------------

def select_target_country(driver, target_country: str):
    """
    Reliably selects target country using Arrow Down + Enter on the dropdown search input,
    with animated virtual cursor guidance and green confirmation flash.
    """
    if not target_country or target_country.lower() in ["united states", "us", "usa"]:
        return

    if HAS_RICH:
        console.print(f"  [dim][*] Configuring geo-target:[/dim] [cyan]{target_country}[/cyan]...")
    else:
        print(f"  [*] Configuring geo-target: {target_country}...")

    driver.execute_script(INJECT_CURSOR_JS)

    try:
        # 1. Locate Country Button
        country_btn = None
        for b in driver.find_elements(By.TAG_NAME, "button"):
            t = b.text.strip()
            if "United States" in t or target_country.lower() in t.lower():
                if "Find keywords" not in t:
                    country_btn = b
                    break

        if not country_btn:
            find_btn = driver.find_element(By.XPATH, "//button[contains(., 'Find keywords')]")
            parent = find_btn.find_element(By.XPATH, "..")
            for b in parent.find_elements(By.TAG_NAME, "button"):
                if "Find keywords" not in b.text and len(b.text.strip()) > 2:
                    country_btn = b
                    break

        if country_btn:
            # Move cursor and click country button
            move_cursor_to(driver, country_btn, click=True)
            country_btn.click()
            time.sleep(1.2)

            # 2. Type into search input with neon focus
            search_inp = driver.find_element(By.CSS_SELECTOR, "input[type='search'], input[placeholder*='Search']")
            move_cursor_to(driver, search_inp, click=True)
            driver.execute_script("""
                arguments[0].focus();
                arguments[0].style.transition = 'all 0.3s ease';
                arguments[0].style.boxShadow = '0 0 16px rgba(0, 229, 255, 0.9)';
                arguments[0].style.borderColor = '#00e5ff';
            """, search_inp)

            search_inp.send_keys(Keys.CONTROL + "a")
            search_inp.send_keys(Keys.BACKSPACE)
            time.sleep(0.2)
            for c in target_country:
                search_inp.send_keys(c)
                time.sleep(random.uniform(0.03, 0.06))

            time.sleep(0.8)

            # Move cursor over the filtered option in the dropdown for visual flair
            select_items = driver.find_elements(By.XPATH, "//*[contains(@class, 'selectItem')]")
            for item in select_items:
                if target_country.lower() in item.text.lower():
                    move_cursor_to(driver, item, click=False)
                    driver.execute_script("""
                        arguments[0].style.transition = 'all 0.25s ease';
                        arguments[0].style.backgroundColor = 'rgba(0, 229, 255, 0.15)';
                    """, item)
                    time.sleep(0.4)
                    break

            # 3. Select via Arrow Down + Enter (Triggers React combobox selection cleanly)
            search_inp.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            search_inp.send_keys(Keys.ENTER)
            time.sleep(1.2)

            # 4. Verify button text & trigger green confirmation flash
            confirmed = False
            for b in driver.find_elements(By.TAG_NAME, "button"):
                if target_country.lower() in b.text.lower():
                    confirmed = True
                    driver.execute_script("""
                        arguments[0].style.transition = 'all 0.4s ease';
                        arguments[0].style.boxShadow = '0 0 25px #00ff88';
                        arguments[0].style.borderColor = '#00ff88';
                        setTimeout(() => {
                            arguments[0].style.boxShadow = '';
                            arguments[0].style.borderColor = '';
                        }, 1800);
                    """, b)
                    break

            if confirmed:
                if HAS_RICH:
                    console.print(f"  [bold green][+][/bold green] [bold white]Geo-target locked:[/bold white] [bold cyan]{target_country}[/bold cyan]\n")
                else:
                    print(f"  [+] Geo-target locked: {target_country}\n")
            else:
                if HAS_RICH:
                    console.print(f"  [dim][*] Target set to:[/dim] [cyan]{target_country}[/cyan]\n")
                else:
                    print(f"  [*] Target set to: {target_country}\n")

    except Exception as e:
        if HAS_RICH:
            console.print(f"  [yellow][!] Country notice: {e}. Continuing...[/yellow]\n")
        else:
            print(f"  [!] Country notice: {e}. Continuing...\n")


# ---------------------------------------------------------------------------
# SEO Analytics & Classification Utilities
# ---------------------------------------------------------------------------

def classify_search_intent(keyword: str, is_question: bool = False) -> str:
    kw = keyword.lower()
    if is_question or any(kw.startswith(q) for q in ["how", "what", "why", "where", "when", "who", "which", "can", "is", "should"]):
        return "Informational"
    if any(w in kw for w in ["how to", "guide", "tutorial", "tips", "ideas", "diy", "meaning"]):
        return "Informational"
    if any(w in kw for w in ["buy", "price", "cost", "cheap", "for sale", "discount", "deal", "order", "shop", "coupon"]):
        return "Transactional"
    if any(w in kw for w in ["best", "top", "review", "vs", "versus", "comparison", "compare", "alternative"]):
        return "Commercial"
    return "General"


def classify_keyword_tail(keyword: str):
    words = keyword.strip().split()
    count = len(words)
    if count <= 2:
        tail = "Short-tail"
    elif count == 3:
        tail = "Mid-tail"
    else:
        tail = "Long-tail"
    return tail, count


def map_estimated_kd(kd_tier: str) -> str:
    kd = (kd_tier or "").lower()
    if "easy" in kd:
        return "0–29 (Easy)"
    elif "medium" in kd:
        return "30–69 (Medium)"
    elif "hard" in kd:
        return "70–84 (Hard)"
    elif "super" in kd:
        return "85–100 (Super Hard)"
    return "Locked / N/A"


def compute_opportunity_score(kd_tier: str, volume: str, word_count: int, intent: str) -> int:
    vol_lower = (volume or "").lower()
    if ">100k" in vol_lower:
        vol_score = 35
    elif ">10,000" in vol_lower or ">10k" in vol_lower:
        vol_score = 30
    elif ">1000" in vol_lower or ">1k" in vol_lower:
        vol_score = 22
    elif ">100" in vol_lower:
        vol_score = 15
    else:
        vol_score = 8

    kd_lower = (kd_tier or "").lower()
    if "easy" in kd_lower:
        kd_score = 40
    elif "medium" in kd_lower:
        kd_score = 22
    elif "hard" in kd_lower:
        kd_score = 5
    else:
        kd_score = 20

    intent_score = 10
    if intent in ["Commercial", "Transactional"]:
        intent_score = 15
    elif intent == "Informational":
        intent_score = 12

    tail_score = 5 if word_count <= 2 else (8 if word_count == 3 else 10)

    total = vol_score + kd_score + intent_score + tail_score
    return min(100, max(1, total))


# ---------------------------------------------------------------------------
# Balanced Seed Priority & Anti-Monopoly Engine
# ---------------------------------------------------------------------------

class SeedManager:
    def __init__(self, initial_seeds: list):
        self.heap = []
        self.seen_seeds = set()
        self.used_subtopics = {}
        self.counter = 0

        for idx, s in enumerate(initial_seeds):
            cleaned = s.strip()
            if cleaned:
                heapq.heappush(self.heap, (-999 + idx, self.counter, cleaned))
                self.counter += 1

    def add_candidate(self, keyword: str, kd_tier: str, volume: str):
        kw_norm = keyword.lower().strip()
        if kw_norm in self.seen_seeds:
            return

        words = kw_norm.split()
        if len(words) > 6 or len(words) < 2:
            return

        base_score = 100
        kd_lower = (kd_tier or "").lower()
        if "easy" in kd_lower:
            base_score += 80
        elif "medium" in kd_lower:
            base_score += 25
        elif "hard" in kd_lower:
            base_score -= 80

        vol_lower = (volume or "").lower()
        if ">100k" in vol_lower:
            base_score += 45
        elif ">10,000" in vol_lower or ">10k" in vol_lower:
            base_score += 30
        elif ">1000" in vol_lower:
            base_score += 15

        for w in words:
            if len(w) > 3 and w in self.used_subtopics:
                base_score -= (self.used_subtopics[w] * 25)

        self.counter += 1
        heapq.heappush(self.heap, (-base_score, self.counter, keyword))

    def pop_next(self):
        while self.heap:
            _, _, seed = heapq.heappop(self.heap)
            seed_clean = seed.strip()
            if seed_clean.lower() not in self.seen_seeds:
                self.seen_seeds.add(seed_clean.lower())
                for w in seed_clean.lower().split():
                    if len(w) > 3:
                        self.used_subtopics[w] = self.used_subtopics.get(w, 0) + 1
                return seed_clean
        return None

    def has_seeds(self):
        return len(self.heap) > 0

    def remaining_count(self):
        return len(self.heap)


# ---------------------------------------------------------------------------
# Extraction & Google Sheets Helpers
# ---------------------------------------------------------------------------

def extract_generator_rows(driver, table_type="Phrase Match", seed_parent=""):
    results = []
    tables = driver.find_elements(By.TAG_NAME, "table")
    
    for table in tables:
        rows = table.find_elements(By.TAG_NAME, "tr")
        for row in rows:
            cols = row.find_elements(By.XPATH, "./th | ./td")
            texts = [c.text.strip().replace("\n", " ") for c in cols]
            
            if not texts or len(texts) < 2:
                continue
            if texts[0].lower() in ["keyword", "keywords"]:
                continue
            
            kw = texts[0]
            kd_tier = texts[1] if len(texts) > 1 else ""
            volume = texts[2] if len(texts) > 2 else ""
            updated = texts[3] if len(texts) > 3 else ""
            
            if "sign up" in kd_tier.lower():
                kd_tier = "Locked"
            if "sign up" in volume.lower():
                volume = "Locked"

            tail_type, word_count = classify_keyword_tail(kw)
            intent = classify_search_intent(kw, is_question=(table_type == "Questions"))
            opp_score = compute_opportunity_score(kd_tier, volume, word_count, intent)
            est_kd = map_estimated_kd(kd_tier)

            results.append({
                "keyword": kw,
                "exact_kd_score": "",
                "kd_tier": kd_tier,
                "estimated_kd_range": est_kd,
                "search_volume": volume,
                "search_intent": intent,
                "keyword_tail": tail_type,
                "word_count": word_count,
                "opportunity_score": opp_score,
                "backlinks_needed": "",
                "topic_cluster": seed_parent,
                "type": table_type,
                "updated": updated
            })
            
    return results


def sync_to_google_sheet(sheet_url: str, rows: list, topic: str = "Keywords", sheet_id: str = None, mode: str = "append"):
    if not sheet_url or not rows:
        return sheet_id, ""
    try:
        payload_rows = []
        for r in rows:
            payload_rows.append({
                "keyword": r.get("keyword", "") or r.get("Target Keyword", ""),
                "opportunity_score": r.get("opportunity_score", "") or r.get("Opp Score", ""),
                "exact_kd": r.get("exact_kd_score", "") or r.get("Exact KD", "") or r.get("estimated_kd_range", ""),
                "kd_tier": r.get("kd_tier", "") or r.get("KD Tier", ""),
                "search_volume": r.get("search_volume", "") or r.get("Search Volume", ""),
                "search_intent": r.get("search_intent", "") or r.get("Search Intent", ""),
                "backlinks_needed": r.get("backlinks_needed", "") or r.get("Backlinks Needed", ""),
                "keyword_tail": r.get("keyword_tail", "") or r.get("Keyword Tail", ""),
                "word_count": r.get("word_count", "") or r.get("Word Count", ""),
                "topic_cluster": r.get("topic_cluster", "") or r.get("Topic Cluster", ""),
                "match_type": r.get("type", "") or r.get("Match Type", "")
            })
        resp = requests.post(
            sheet_url,
            json={
                "topic": topic,
                "sheet_id": sheet_id,
                "mode": mode,
                "rows": payload_rows
            },
            timeout=15
        )
        if resp.status_code == 200:
            res_data = resp.json()
            new_id = res_data.get("sheet_id", sheet_id)
            new_url = res_data.get("sheet_url", "")
            return new_id, new_url
    except Exception:
        pass
    return sheet_id, ""



# ---------------------------------------------------------------------------
# Stage 2: Exact Numeric KD & Backlink Lookup
# ---------------------------------------------------------------------------

def enrich_exact_kd(driver, keywords_list: list, output_path: str, master_list: list, sheet_url: str = None, sheet_id: str = None):
    if not keywords_list:
        return {}

    kd_results = {}
    url = "https://ahrefs.com/keyword-difficulty"
    total_count = len(keywords_list)

    if HAS_RICH:
        console.rule("[bold magenta] Stage 2: Exact Numeric KD & Backlink Audit [/bold magenta]", style="magenta")
        console.print(f"  [dim]Auditing difficulty and backlinks for {total_count} priority keywords...[/dim]\n")
    else:
        print(f"\nStage 2: Exact Numeric KD & Backlink Audit ({total_count} Keywords)\n")

    driver.uc_open_with_reconnect(url, reconnect_time=4)
    time.sleep(3)
    handle_cookie_banner(driver)

    for idx, kw in enumerate(keywords_list):
        pct = ((idx + 1) / total_count) * 100

        try:
            inp = driver.find_element(By.CSS_SELECTOR, "input[placeholder*='keyword'], input[placeholder*='Enter']")
            human_type_animated(driver, inp, kw)

            btn = None
            for b in driver.find_elements(By.TAG_NAME, "button"):
                if any(t in b.text for t in ["Check keyword", "Check"]):
                    btn = b
                    break
            
            if btn:
                highlight_and_click(driver, btn)
            else:
                inp.send_keys(Keys.ENTER)

            time.sleep(4.5)
            wait_and_solve_turnstile(driver)

            exact_kd = "N/A"
            chart_vals = driver.find_elements(By.CSS_SELECTOR, "div[class*='chartValue']")
            for cv in chart_vals:
                t = cv.text.strip()
                if t.isdigit():
                    exact_kd = t
                    break

            backlinks = "N/A"
            match = re.search(r"backlinks from ~?([0-9,]+) websites", driver.page_source, re.IGNORECASE)
            if match:
                backlinks = f"~{match.group(1)} websites"

            kd_results[kw] = {
                "exact_kd": exact_kd,
                "backlinks": backlinks
            }

            if HAS_RICH:
                kd_color = "green" if exact_kd.isdigit() and int(exact_kd) <= 15 else ("yellow" if exact_kd.isdigit() and int(exact_kd) <= 40 else "red")
                tier_str = "Easy" if exact_kd.isdigit() and int(exact_kd) <= 29 else ("Medium" if exact_kd.isdigit() and int(exact_kd) <= 69 else "Hard")
                console.print(f"  [dim][{idx+1:02d}/{total_count:02d}][/dim] [bold white]\"{kw}\"[/bold white]  [dim]→[/dim]  KD: [{kd_color} bold]{exact_kd}/100[/{kd_color} bold] [dim]({tier_str})[/dim]  [dim]│[/dim]  Backlinks: [blue bold]{backlinks}[/blue bold]")
            else:
                print(f"  [{idx+1:02d}/{total_count:02d}] \"{kw}\" -> KD: {exact_kd}/100 | Backlinks: {backlinks}")

            # Close modal
            close_btns = driver.find_elements(By.CSS_SELECTOR, "button[aria-label*='Close'], button[class*='close']")
            for cb in close_btns:
                try:
                    driver.execute_script("arguments[0].click();", cb)
                    break
                except Exception:
                    pass
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

            # Continuous Autosave
            for row in master_list:
                if row["keyword"] == kw:
                    row["exact_kd_score"] = exact_kd
                    row["backlinks_needed"] = backlinks
                    break
            
            df_temp = pd.DataFrame(master_list)
            df_temp.to_csv(output_path, index=False, encoding="utf-8-sig")

            # Real-time single-keyword badge illumination in Google Sheets
            if sheet_url and sheet_id:
                try:
                    requests.post(
                        sheet_url,
                        json={
                            "action": "update_keyword",
                            "sheet_id": sheet_id,
                            "keyword": kw,
                            "exact_kd": exact_kd,
                            "backlinks": backlinks
                        },
                        timeout=5
                    )
                except Exception:
                    pass

            time.sleep(random.uniform(2.5, 4.0))

        except Exception:
            kd_results[kw] = {"exact_kd": "Error", "backlinks": "N/A"}
            time.sleep(2)

    return kd_results


# ---------------------------------------------------------------------------
# Main Orchestrator
# ---------------------------------------------------------------------------

def run_harvester(
    seed_keywords: list,
    quota: int = 50,
    country: str = "United States",
    include_questions: bool = True,
    enrich_kd_count: int = 10,
    sheet_url: str = None,
    output_path: str = None
):
    print_banner()

    primary_seed = seed_keywords[0]
    safe_seed = "".join([c if c.isalnum() else "-" for c in primary_seed]).strip("-").lower()
    while "--" in safe_seed:
        safe_seed = safe_seed.replace("--", "-")

    user_custom_output = bool(output_path)
    if not output_path:
        output_path = f"{safe_seed}-{quota}-keywords.csv"

    enrich_display = "ALL Harvested Keywords" if enrich_kd_count == -1 else (f"Top {enrich_kd_count} Winners" if enrich_kd_count > 0 else "None (Skipped)")
    print_config_panel(seed_keywords, quota, country, enrich_display, sheet_url, output_path)

    seed_manager = SeedManager(seed_keywords)
    harvested_keywords = []
    seen_keywords = set()
    active_sheet_id = None
    active_sheet_url = None

    profile_dir = os.path.abspath("./chrome_profile")
    if HAS_RICH:
        console.print("[dim][*] Launching Stealth Chrome Core (Persistent Session Profile)...[/dim]")
    driver = Driver(uc=True, headless=False, user_data_dir=profile_dir)

    try:
        try:
            driver.set_window_size(1366, 900)
        except Exception:
            pass

        gen_url = "https://ahrefs.com/keyword-generator"
        driver.uc_open_with_reconnect(gen_url, reconnect_time=4)
        time.sleep(2.5)
        handle_cookie_banner(driver)

        # Country selection
        select_target_country(driver, country)

        searches_done = 0

        while seed_manager.has_seeds() and len(harvested_keywords) < quota:
            current_seed = seed_manager.pop_next()
            if not current_seed:
                break

            searches_done += 1
            progress_pct = (len(harvested_keywords) / quota) * 100

            if HAS_RICH:
                console.print(f"[bold cyan]⚡ [{len(harvested_keywords):02d}/{quota:02d}][/bold cyan] [bold white]Searching:[/bold white] [bold yellow]\"{current_seed}\"[/bold yellow]  [dim]│  Queue: {seed_manager.remaining_count()} seeds[/dim]")
            else:
                print(f"[{len(harvested_keywords):02d}/{quota:02d}] Searching: \"{current_seed}\" | Queue: {seed_manager.remaining_count()} seeds")

            # 1. Type Seed with visual animation & cursor
            inp = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Enter keyword"]')
            human_type_animated(driver, inp, current_seed)

            # 2. Click Find keywords with visual pulse
            find_btn = None
            for btn in driver.find_elements(By.TAG_NAME, "button"):
                if "Find keywords" in btn.text:
                    find_btn = btn
                    break

            if find_btn:
                highlight_and_click(driver, find_btn)
            else:
                inp.send_keys(Keys.ENTER)

            time.sleep(2)
            wait_and_solve_turnstile(driver)
            time.sleep(1.5)

            # If table is not visible yet, retry clicking Find keywords or wait
            tables = driver.find_elements(By.TAG_NAME, "table")
            if not tables:
                time.sleep(2)
                tables = driver.find_elements(By.TAG_NAME, "table")
                if not tables and find_btn:
                    try:
                        find_btn.click()
                        time.sleep(3)
                        wait_and_solve_turnstile(driver)
                    except Exception:
                        pass

            # True modal table scrolling animation
            smooth_scroll_table(driver)

            new_this_round = 0
            intent_counts = {"Informational": 0, "Commercial": 0, "Transactional": 0, "General": 0}

            # 3. Extract Phrase Match
            pm_batch = extract_generator_rows(driver, table_type="Phrase Match", seed_parent=current_seed)
            for item in pm_batch:
                kw = item["keyword"]
                kw_norm = kw.lower().strip()
                if kw_norm not in seen_keywords:
                    seen_keywords.add(kw_norm)
                    harvested_keywords.append(item)
                    new_this_round += 1
                    intent_counts[item["search_intent"]] = intent_counts.get(item["search_intent"], 0) + 1
                    seed_manager.add_candidate(kw, item["kd_tier"], item["search_volume"])

                if len(harvested_keywords) >= quota:
                    break

            # 4. Extract Questions Tab
            if include_questions and len(harvested_keywords) < quota:
                try:
                    q_tabs = [b for b in driver.find_elements(By.TAG_NAME, "button") if "Questions" in b.text]
                    if q_tabs:
                        highlight_and_click(driver, q_tabs[0])
                        time.sleep(2.5)
                        q_batch = extract_generator_rows(driver, table_type="Questions", seed_parent=current_seed)
                        for item in q_batch:
                            kw = item["keyword"]
                            kw_norm = kw.lower().strip()
                            if kw_norm not in seen_keywords:
                                seen_keywords.add(kw_norm)
                                harvested_keywords.append(item)
                                new_this_round += 1
                                intent_counts[item["search_intent"]] = intent_counts.get(item["search_intent"], 0) + 1
                                seed_manager.add_candidate(kw, item["kd_tier"], item["search_volume"])
                            if len(harvested_keywords) >= quota:
                                break

                        pm_tabs = [b for b in driver.find_elements(By.TAG_NAME, "button") if "Phrase match" in b.text]
                        if pm_tabs:
                            highlight_and_click(driver, pm_tabs[0])
                            time.sleep(0.5)
                except Exception:
                    pass

            if HAS_RICH:
                console.print(f"   [green]↳ Harvested +{new_this_round} unique keywords[/green]  [dim]│[/dim]  [dim]Intent:[/dim] [green]Info: {intent_counts['Informational']}[/green] [dim]·[/dim] [yellow]Comm: {intent_counts['Commercial']}[/yellow] [dim]·[/dim] [cyan]Trans: {intent_counts['Transactional']}[/cyan]\n")
            else:
                print(f"   ↳ Harvested +{new_this_round} unique keywords | Intent: Info: {intent_counts['Informational']} Comm: {intent_counts['Commercial']} Trans: {intent_counts['Transactional']}\n")

            # Checkpoint autosave
            if harvested_keywords:
                df = pd.DataFrame(harvested_keywords)
                df.to_csv(output_path, index=False, encoding="utf-8-sig")
                if sheet_url and new_this_round > 0:
                    active_sheet_id, active_sheet_url = sync_to_google_sheet(
                        sheet_url,
                        harvested_keywords[-new_this_round:],
                        topic=primary_seed,
                        sheet_id=active_sheet_id,
                        mode="append"
                    )

            time.sleep(random.uniform(2.0, 3.5))

        # Stage 2: Exact Numeric KD Lookup
        if enrich_kd_count != 0 and harvested_keywords:
            harvested_keywords.sort(key=lambda x: x["opportunity_score"], reverse=True)
            
            if enrich_kd_count == -1 or enrich_kd_count >= len(harvested_keywords):
                candidates = [x["keyword"] for x in harvested_keywords]
            else:
                candidates = [x["keyword"] for x in harvested_keywords[:enrich_kd_count]]

            exact_data = enrich_exact_kd(driver, candidates, output_path, harvested_keywords, sheet_url=sheet_url, sheet_id=active_sheet_id)
            
            for row in harvested_keywords:
                kw = row["keyword"]
                if kw in exact_data:
                    row["exact_kd_score"] = exact_data[kw]["exact_kd"]
                    row["backlinks_needed"] = exact_data[kw]["backlinks"]

        # Final Export & Formatting (12-Column SEO Intelligence Architecture)
        actual_count = len(harvested_keywords)
        if not user_custom_output:
            final_output_path = f"{safe_seed}-{actual_count}-keywords.csv"
        else:
            final_output_path = output_path

        if harvested_keywords:
            df = pd.DataFrame(harvested_keywords)
            if "opportunity_score" in df.columns:
                df.sort_values(by="opportunity_score", ascending=False, inplace=True)

            # Insert # Rank column
            df.reset_index(drop=True, inplace=True)
            df.insert(0, "#", df.index + 1)

            # Clean and reorder into the 12-column architecture
            rename_map = {
                "keyword": "Target Keyword",
                "opportunity_score": "Opp Score",
                "exact_kd_score": "Exact KD",
                "kd_tier": "KD Tier",
                "search_volume": "Search Volume",
                "search_intent": "Search Intent",
                "backlinks_needed": "Backlinks Needed",
                "keyword_tail": "Keyword Tail",
                "word_count": "Word Count",
                "topic_cluster": "Topic Cluster",
                "type": "Match Type"
            }
            ordered_cols = [
                "#", "Target Keyword", "Opp Score", "Exact KD", "KD Tier",
                "Search Volume", "Search Intent", "Backlinks Needed", "Keyword Tail",
                "Word Count", "Topic Cluster", "Match Type"
            ]
            export_df = df.rename(columns=rename_map)
            export_cols = [c for c in ordered_cols if c in export_df.columns]
            export_df = export_df[export_cols]
            export_df.to_csv(final_output_path, index=False, encoding="utf-8-sig")

            if output_path != final_output_path and os.path.exists(output_path):
                try:
                    os.remove(output_path)
                except Exception:
                    pass

            # Final Google Sheets Sync (overwrite with final sorted & enriched intelligence data)
            if sheet_url and not df.empty:
                if HAS_RICH:
                    console.print("  [dim][*] Finalizing Google Sheets intelligence dashboard...[/dim]")
                else:
                    print("  [*] Finalizing Google Sheets intelligence dashboard...")
                active_sheet_id, active_sheet_url = sync_to_google_sheet(
                    sheet_url,
                    harvested_keywords,
                    topic=primary_seed,
                    sheet_id=active_sheet_id,
                    mode="replace" if active_sheet_id else "append"
                )
        else:
            df = pd.DataFrame()

        if HAS_RICH:
            console.print()
            if not df.empty:
                t = Table(
                    title="Top Keywords Ranked by AI Opportunity Score",
                    caption="✦ Ahrefs Auto Scraper v3.5 • Engineered by Al Hossain Rifat ✦",
                    border_style="cyan",
                    box=box.ROUNDED,
                    header_style="bold cyan"
                )
                t.add_column("Rank", style="bold dim", width=5, no_wrap=True)
                t.add_column("Keyword", style="bold white")
                t.add_column("Exact KD", style="bold magenta", justify="center", no_wrap=True)
                t.add_column("KD Tier", style="magenta", no_wrap=True)
                t.add_column("Volume", style="green", justify="right", no_wrap=True)
                t.add_column("Intent", style="yellow", no_wrap=True)
                t.add_column("Opp Score", style="bold red", justify="center", no_wrap=True)
                t.add_column("Backlinks", style="blue")

                preview_count = min(15, len(df))
                for rank_idx, (_, r) in enumerate(df.head(preview_count).iterrows(), start=1):
                    kd_val = str(r["exact_kd_score"]) if r["exact_kd_score"] else "-"
                    t.add_row(
                        f"#{rank_idx}",
                        str(r["keyword"]),
                        kd_val,
                        str(r["kd_tier"]),
                        str(r["search_volume"]),
                        str(r["search_intent"]),
                        f"{r['opportunity_score']}/100",
                        str(r["backlinks_needed"]) if r["backlinks_needed"] else "-"
                    )
                console.print(t)
                console.print()

            if not df.empty:
                sheet_line = f"\n[bold white]Live Google Sheet:[/bold white] [bold cyan underline]{active_sheet_url}[/bold cyan underline]" if active_sheet_url else ""
                summary = Panel(
                    f"[bold green]✔ Complete![/bold green] Successfully harvested [bold cyan]{actual_count}[/bold cyan] unique keywords across [bold yellow]{searches_done}[/bold yellow] search queries.\n"
                    f"[bold white]Export File:[/bold white] [underline yellow]{final_output_path}[/underline yellow]{sheet_line}\n"
                    f"[dim italic]Engineered by Al Hossain Rifat[/dim italic]",
                    border_style="green",
                    box=box.ROUNDED
                )
                console.print(summary)
            else:
                warn_panel = Panel(
                    f"[bold yellow]Notice:[/bold yellow] No keywords were harvested during this session.\n"
                    f"[white]If Cloudflare verification appeared, solve it once so your session token is saved in [cyan]./chrome_profile[/cyan].[/white]\n"
                    f"[dim italic]Engineered by Al Hossain Rifat[/dim italic]",
                    border_style="yellow",
                    box=box.ROUNDED
                )
                console.print(warn_panel)
            console.print()
        else:
            if not df.empty:
                print(f"\n[COMPLETE] Successfully harvested {len(harvested_keywords)} keywords into {final_output_path}")
                if active_sheet_url:
                    print(f"[LIVE SHEET] {active_sheet_url}")
            else:
                print("\n[NOTICE] No keywords were harvested. Check if Cloudflare blocked the search.")
            print("Engineered by Al Hossain Rifat\n")

    finally:
        if HAS_RICH:
            console.print("[dim][*] Closing browser session...[/dim]")
        driver.quit()


def load_saved_sheet_url():
    for config_file in ["config/sheet_config.json", "sheet_config.json"]:
        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    val = data.get("sheet_url", "").strip()
                    if val:
                        return val
            except Exception:
                pass
    return ""


def save_sheet_url(url: str):
    config_dir = "config"
    os.makedirs(config_dir, exist_ok=True)
    config_file = os.path.join(config_dir, "sheet_config.json")
    try:
        import json
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump({"sheet_url": url.strip()}, f, indent=2)
    except Exception:
        pass



def main():
    parser = argparse.ArgumentParser(description="Ahrefs Auto Scraper (Made by Al Hossain Rifat)")
    parser.add_argument("-s", "--seed", type=str, help="Initial seed keyword(s), comma-separated (e.g. 'smart watch, fitness band')")
    parser.add_argument("-q", "--quota", type=int, default=50, help="Target keyword quota (default: 50)")
    parser.add_argument("-c", "--country", type=str, default="United States", help="Target country (e.g. 'United States', 'United Kingdom', 'Canada')")
    parser.add_argument("--enrich-kd", type=str, default="10", help="Number of top keywords to look up exact 0-100 KD for, or 'all' (default: 10, set 0 to skip)")
    parser.add_argument("--enrich-all", action="store_true", help="Look up exact 0-100 KD & backlinks for ALL harvested keywords")
    parser.add_argument("--sheet-url", type=str, default="", help="Google Apps Script Webhook URL for live Google Sheets sync")
    parser.add_argument("-o", "--output", type=str, default="", help="Custom output CSV filename")
    parser.add_argument("--no-questions", action="store_true", help="Exclude the Questions tab")

    args = parser.parse_args()

    saved_url = load_saved_sheet_url()
    sheet_url = args.sheet_url.strip() if args.sheet_url else saved_url
    if args.sheet_url:
        save_sheet_url(args.sheet_url.strip())

    seed_raw = args.seed
    quota = args.quota
    country = args.country

    if args.enrich_all:
        enrich_kd = -1
    elif str(args.enrich_kd).lower() == "all":
        enrich_kd = -1
    else:
        try:
            enrich_kd = int(args.enrich_kd)
        except ValueError:
            enrich_kd = 10

    if not seed_raw:
        print_banner()
        seed_raw = input("Enter seed keyword(s) [e.g. 'smart watch, fitness band']: ").strip()
        if not seed_raw:
            seed_raw = "smart watch"
            print(f"Defaulting to: '{seed_raw}'")

        quota_str = input(f"Enter target quota of keywords [default: 50]: ").strip()
        quota = int(quota_str) if quota_str.isdigit() else 50

        country_input = input(f"Target country [default: United States]: ").strip()
        if country_input:
            country = country_input

        enrich_str = input(f"Look up exact 0-100 KD for how many keywords? [number, or 'all', default: 10]: ").strip()
        if enrich_str.lower() == "all":
            enrich_kd = -1
        elif enrich_str.isdigit():
            enrich_kd = int(enrich_str)
        else:
            enrich_kd = 10

        if saved_url:
            short_url = saved_url[:30] + "..." + saved_url[-12:]
            sheet_input = input(f"Google Sheets Webhook [Press Enter for saved '{short_url}', or type 'none']: ").strip()
            if sheet_input.lower() == "none":
                sheet_url = ""
            elif sheet_input:
                sheet_url = sheet_input
                save_sheet_url(sheet_url)
            else:
                sheet_url = saved_url
        else:
            sheet_input = input("Google Sheets Webhook URL [optional, press Enter to skip]: ").strip()
            if sheet_input:
                sheet_url = sheet_input
                save_sheet_url(sheet_url)
            else:
                sheet_url = ""

    seed_list = [s.strip() for s in seed_raw.split(",") if s.strip()]

    run_harvester(
        seed_keywords=seed_list,
        quota=quota,
        country=country,
        include_questions=not args.no_questions,
        enrich_kd_count=enrich_kd,
        sheet_url=sheet_url or None,
        output_path=args.output or None
    )


if __name__ == "__main__":
    main()
