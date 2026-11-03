import requests
from bs4 import BeautifulSoup

# وضع التوكن مباشرة
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
    print("Checking Vox Cinemas movie page via Requests...")
    url = "https://egy.voxcinemas.com/movies/avengers-doomsday-infinity-vision"
    
    # محاكاة متصفح حقيقي لتجاوز الحماية
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apgx,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            page_content = soup.get_text().lower()
            
            # استهداف تاريخ 25 ديسمبر بالتحديد
            target_date = "25 dec"
            
            if target_date in page_content:
                message = "🚨 *تنبيه هام جداً!* \n\nتم رصد فتح حجز يوم *Friday 25 Dec* لفيلم *Avengers: Doomsday* على فوكس سينما مصر! الحق احجز الآن! 🎬🔥"
                send_telegram_alert(message)
            else:
                print("Booking for 'Fri 25 Dec' not available yet.")
                status_message = "🤖 *تحديث بوت فوكس:* \n\nتم فحص صفحة الفيلم بنجاح، حجز يوم *25 Dec* لم يُفتح بعد. جارٍ المتابعة المستمرة... ⏳"
                send_telegram_alert(status_message)
        else:
            error_message = f"⚠️ *تنبيه خطأ في بوت فوكس:* \n\nفشل الاتصال بالموقع، كود الاستجابة: {response.status_code}"
            send_telegram_alert(error_message)
            
    except Exception as e:
        error_message = f"⚠️ *تنبيه خطأ في بوت فوكس:* \n\nحدث استثناء أثناء جلب الصفحة: {str(e)}"
        send_telegram_alert(error_message)
        print(f"حدث خطأ: {e}")

if __name__ == "__main__":
    check_vox_movies()
