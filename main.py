import os
import re
import time
import requests
from playwright.sync_api import sync_playwright

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_IDS = ["1152120052", "1932248872"]
URL = "https://egy.voxcinemas.com/movies/avengers-doomsday-infinity-vision"

def send_telegram_alert(message):
    for chat_id in CHAT_IDS:
        try:
            r = requests.post(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                json={"chat_id": chat_id, "text": message, "parse_mode": "Markdown"},
                timeout=20,
            )
            print(f"Telegram {chat_id}: {r.status_code}")
        except Exception as e:
            print(f"Error sending request: {e}")

def fetch_page_text():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage",
                  "--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            timezone_id="Africa/Cairo",
            extra_http_headers={"Accept-Language": "en-US,en;q=0.9,ar;q=0.8"},
        )
        page = context.new_page()
        try:
            page.goto(URL, timeout=45000, wait_until="domcontentloaded")
            page.wait_for_timeout(6000)
            return page.inner_text("body").lower()
        finally:
            browser.close()

def check_vox_movies():
    last_error = None
    for attempt in range(1, 4):
        try:
            print(f"Attempt {attempt}...")
            text = fetch_page_text()
            if re.search(r"25\s*dec", text):
                send_telegram_alert(
                    "🚨 *تنبيه هام جداً!*\n\nتم رصد فتح حجز يوم *Fri 25 Dec* "
                    "لفيلم *Avengers: Doomsday* على فوكس سينما مصر! 🎬🔥"
                )
            else:
                print("25 Dec not available yet.")
            return
        except Exception as e:
            last_error = e
            print(f"Attempt {attempt} failed: {e}")
            time.sleep(10)

    print(f"All attempts failed: {last_error}")
    # Make the job fail visibly instead of showing a fake green check
    raise SystemExit(1)

if __name__ == "__main__":
    check_vox_movies()
