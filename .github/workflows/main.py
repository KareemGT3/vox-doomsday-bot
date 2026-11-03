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
    print("Starting Playwright to check Vox Cinemas...")
    with sync_playwright() as p:
        # تشغيل المتصفح مع إعدادات تحاكي متصفح حقيقي لتجنب الحظر
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        try:
            # الدخول على الموقع الرئيسي لفوكس سينما مصر أولاً
            print("جارٍ تصفح موقع فوكس سينما مصر...")
            page.goto("https://egypt.voxcinemas.com/", timeout=60000, wait_until="domcontentloaded")
            page.wait_for_timeout(5000)
            
            # محاولة الانتقال لصفحة الأفلام أو البحث
            page_content = page.content().lower()
            
            # كلمة البحث عن الفيلم
            target_movie = "avengers: doomsday"
            
            if target_movie in page_content:
                message = "🚨 *تنبيه هام جداً!* \n\nتم رصد حجز فيلم *Avengers: Doomsday* على موقع فوكس سينما مصر! الحق احجز الآن! 🎬🔥"
                send_telegram_alert(message)
            else:
                print("Movie 'Avengers: Doomsday' not available for booking yet.")
                
        except Exception as e:
            print(f"حدث خطأ أثناء تصفح الموقع: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    check_vox_movies()
