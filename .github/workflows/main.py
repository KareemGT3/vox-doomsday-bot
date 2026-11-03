import requests
from playwright.sync_api import sync_playwright

# بيانات التليجرام الخاصة بك
TELEGRAM_TOKEN = "905997430:AAFULCudI3gIep-C1HuFG2DiVwJDJrj0_2I"
CHAT_ID = "1152120052"
MOVIE_URL = "https://egy.voxcinemas.com/movies/avengers-doomsday"


def send_telegram_notification(message):
  url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
  payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
  try:
    requests.post(url, json=payload)
  except Exception as e:
    print(f"Error sending telegram message: {e}")


def check_movie_booking():
  print("جاري فحص صفحة الفيلم...")
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    ).new_page()

    try:
      page.goto(MOVIE_URL, timeout=60000)
      page.wait_for_load_state("networkidle")

      page_text = page.inner_text("body").lower()
      page_html = page.content().lower()
      browser.close()

      target_date_found = (
          "25" in page_text and "dec" in page_text
      ) or "25 ديسمبر" in page_text
      booking_open = (
          "book" in page_text
          or "حجز" in page_text
          or "showtimes" in page_html
          or "مواعيد" in page_text
      )

      if target_date_found and booking_open:
        msg = (
            "🎉 **الحجز فتح لـ Doomsday!**\n\nتم رصد إتاحة حجز يوم **الجمعة 25"
            f" ديسمبر** على موقع فوكس سينما.\n\nرابط الفيلم المباشر:\n{MOVIE_URL}"
        )
        send_telegram_notification(msg)
        print("تم العثور على الحجز وإرسال التنبيه!")
        return True
      else:
        print("لم يتم رصد فتح الحجز ليوم 25 ديسمبر حتى الآن...")

    except Exception as e:
      print(f"حدث خطأ أثناء تصفح الموقع: {e}")
      try:
        browser.close()
      except:
        pass

  return False


if __name__ == "__main__":
  check_movie_booking()
