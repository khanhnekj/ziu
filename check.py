import requests
import threading
import random

ACC_FILE = "acc.txt"
LIVE_FILE = "live.txt"
DIE_FILE = "die.txt"
PRX_FILE = "prx.txt"

THREADS = 50

lock = threading.Lock()


# lấy proxy từ proxyscrape
def scrape_proxy():
    print("[*] Đang tải proxy...")
    url = "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all"

    r = requests.get(url)
    proxies = r.text.split("\n")

    with open(PRX_FILE, "w") as f:
        for p in proxies:
            if ":" in p:
                f.write(p.strip() + "\n")

    print(f"[+] Đã lưu {len(proxies)} proxy")


def load_proxy():
    with open(PRX_FILE) as f:
        return [p.strip() for p in f if ":" in p]


def load_acc():
    with open(ACC_FILE) as f:
        return [a.strip() for a in f if "|" in a]


def get_proxy(proxy_list):
    p = random.choice(proxy_list)
    return {
        "http": "http://" + p,
        "https": "http://" + p
    }


def check(acc, proxy_list):
    email, password = acc.split("|")
    proxy = get_proxy(proxy_list)

    try:
        r = requests.get(
            "https://httpbin.org/ip",
            proxies=proxy,
            timeout=10
        )

        print(f"[LIVE] {email} | {proxy['http']}")

        with lock:
            with open(LIVE_FILE, "a") as f:
                f.write(acc + "\n")

    except:
        print(f"[DIE] {email}")

        with lock:
            with open(DIE_FILE, "a") as f:
                f.write(acc + "\n")


def worker(acc_list, proxy_list):
    while acc_list:
        try:
            acc = acc_list.pop()
        except:
            break
        check(acc, proxy_list)


def main():
    scrape_proxy()

    proxy_list = load_proxy()
    acc_list = load_acc()

    threads = []

    for _ in range(THREADS):
        t = threading.Thread(target=worker, args=(acc_list, proxy_list))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print("[✓] Done")


if __name__ == "__main__":
    main()