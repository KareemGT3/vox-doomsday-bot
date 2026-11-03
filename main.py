تفضل يا كريم! تم تحديث السكريبت كاملاً وإضافة الـ Chat ID الخاص بك (1152120052) والـ Chat ID الخاص بصاحبك (1932248872) داخل القائمة CHAT_IDS لكي تصلكم التنبيهات معاً في نفس اللحظة فور توفر الحجز:
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
        # تشغيل المتصفح في الخلفية
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # رابط موقع فوكس سينما مصر (أو صفحة البحث الخاصة بالفيلم)
            page.goto("https://egypt.voxcinemas.com/", timeout=60000)
            page.wait_for_timeout(5000) # انتظار تحميل الصفحة بالكامل
            
            page_content = page.content().lower()
            
            # كلمة البحث عن الفيلم
            target_movie = "avengers: doomsday"
            
            if target_movie in page_content:
                message = "🚨 *تنبيه هام جداً!* \n\nتم رصد حجز فيلم *Avengers: Doomsday* على موقع فوكس سينما مصر! الحق احجز الآن! 🎬🔥"
                send_telegram_alert(message)
            else:
                print("Movie 'Avengers: Doomsday' not available for booking yet.")
                
        except Exception as e:
            print(f"An error occurred while scraping: {e}")
            
        finally:
            browser.close()

if __name__ == "__main__":
    check_vox_movies()

الخطوة الأخيرة:
 * انسخ الكود أعلاه بالكامل.
 * توجه إلى ملف main.py في مستودع GitHub الخاص بك.
 * الصق الكود واضغط على Commit changes لحفظ التعديلات.
بكده السكريبت جاهز تماماً وهيبعت التنبيه ليك إنت وصاحبك مع بعض أوتوماتيكياً. بالتوفيق يا بطل وإن شاء الله تلحقوا الحجز أول ما ينزل!
