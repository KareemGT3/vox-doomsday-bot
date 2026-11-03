import os
import requests
from playwright.sync_api import sync_playwright

# وضع التوكن مباشرة هنا لتجنب أي مشاكل في قراءته من جيت هب
TOKEN = "9059974930:AAFULCudI3gIep-C1HufG2dIVwJDJrjO_2I"

# قائمة الـ Chat IDs الخاصة بك وبصاحبك
CHAT_IDS = ["1152120052", "1932248872"]

def send_telegram_alert(message):
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
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-http2", 
                "--no-sandbox", 
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-accelerated-2d-canvas",
                "--disable-gpu"
            ]
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800}
        )
        page = context.new_page()
        
        try:
            print("جارٍ تصفح صفحة فيلم Avengers: Doomsday على فوكس سينما...")
            # استخدام 'commit' لتجاوز مشاكل الانتظار الطويل وتحميل الصفحة بسرعة
            page.goto("https://egy.voxcinemas.com/movies/avengers-doomsday-infinity-vision", timeout=60000, wait_until="commit")
            
            # الانتظار حتى تظهر النصوص الأساسية أو مرور ثوانٍ آمنة
            page.wait_for_timeout(8000)
            
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
