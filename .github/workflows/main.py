import os
import requests
from playwright.sync_api import sync_playwright

# توكن البوت يتم جلبه من متغيرات الأمان في جيت هب
TOKEN = os.environ.get("TELEGRAM_TOKEN")

# قائمة الـ Chat IDs الخاصة بك وبصاحبك
CHAT_IDS = ["1152120052", "1932248872"]

def send_telegram_alert(message):
    if not TOKEN:
        print("Telegram token not found!")
        return
        
    for chat_id in CHAT_IDS:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                print(f"Alert sent successfully to chat_id: {chat_id}")
            else:
                print(f"Failed to send alert to {chat_id}: {response.text}")
        except Exception as e:
            print(f"Error sending request: {e}")

def check_vox_movies():
    print("Starting Playwright to check Vox Cinemas movie page...")
    with sync_playwright() as p:
        # إضافة args لتجاوز مشاكل بروتوكول HTTP/2 وتجنب الحظر
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-http2", "--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            print("جارٍ تصفح صفحة فيلم Avengers: Doomsday على فوكس سينما...")
            page.goto("https://egy.voxcinemas.com/movies/avengers-doomsday-infinity-vision", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(6000)
            
            page_content = page.content().lower()
            
            # استهداف تاريخ 25 ديسمبر بالتحديد
            target_date = "25 dec"
            
            if target_date in page_content:
                message = "🚨 *تنبيه هام جداً!* \n\nتم رصد فتح حجز يوم *Friday 25 Dec* لفيلم *Avengers: Doomsday* على فوكس سينما مصر! الحق احجز الآن! 🎬🔥"
                send_telegram_alert(message)
            else:
                print("Booking for 'Fri 25 Dec' not available yet.")
                status_message = "🤖 *تحديث بوت فوكس:* \n\nتم فحص صفحة الفيلم بنجاح، حجز يوم *25 Dec* لم يُفتح بعد. جارٍ المتابعة المستمرة... ⏳"
                send_telegram_alert(status_message)
                
        except Exception as e:
            error_message = f"⚠️ *تنبيه خطأ في بوت فوكس:* \n\nحدث استثناء أثناء تصفح صفحة الفيلم: {str(e)}"
            send_telegram_alert(error_message)
            print(f"حدث خطأ أثناء تصفح الموقع: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    check_vox_movies()
