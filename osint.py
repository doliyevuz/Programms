import requests
import os
import threading
from queue import Queue
from colorama import Fore, Style, init

init(autoreset=True)

SITES = {
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Twitter/X": "https://twitter.com/{}",
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Reddit": "https://www.reddit.com/user/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Twitch": "https://www.twitch.tv/{}",
    "YouTube": "https://www.youtube.com/@{}",
    "Medium": "https://medium.com/@{}",
    "SoundCloud": "https://soundcloud.com/{}",
    "Steam": "https://steamcommunity.com/id/{}",
    "HackerRank": "https://www.hackerrank.com/{}",
    "Codeforces": "https://codeforces.com/profile/{}",
    "VK": "https://vk.com/{}",
    "OK": "https://ok.ru/{}",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

found = []
not_found = []

def clear():
    os.system("clear" if os.name == "posix" else "cls")

def check_username(site, url, username):
    try:
        r = requests.get(url.format(username), headers=HEADERS, timeout=7)
        if r.status_code == 200 and "not found" not in r.text.lower():
            print(Fore.GREEN + f"[+] TOPILDI  | {site} → {url.format(username)}")
            found.append(site)
        else:
            print(Fore.RED + f"[-] YO‘Q     | {site}")
            not_found.append(site)
    except:
        print(Fore.YELLOW + f"[!] XATO     | {site}")
        not_found.append(site)

def worker(q, username):
    while not q.empty():
        site, url = q.get()
        check_username(site, url, username)
        q.task_done()

def start_scan(username):
    q = Queue()
    for site, url in SITES.items():
        q.put((site, url))

    threads = []
    for _ in range(10):
        t = threading.Thread(target=worker, args=(q, username))
        t.start()
        threads.append(t)

    q.join()

def menu():
    clear()
    print("""
╔════════════════════════════════════╗
║        🔍 USERNAME OSINT           ║
╠════════════════════════════════════╣
║  1️⃣  Username tekshirish            ║
║  0️⃣  Chiqish                        ║
╚════════════════════════════════════╝
""")

while True:
    menu()
    choice = input("➜ Tanlang: ").strip()

    if choice == "1":
        clear()
        print("""
╔════════════════════════════════════╗
║        🔎 TEKSHIRUV OYNASI         ║
╚════════════════════════════════════╝
""")
        username = input("Username kiriting ➜ ").strip()

        found.clear()
        not_found.clear()

        print("\n⏳ Qidiruv boshlandi...\n")
        start_scan(username)

        print("\n════════ NATIJA ════════")
        print(f"✅ Topildi: {len(found)}")
        print(f"❌ Topilmadi: {len(not_found)}")

        input("\n↩️  Menyuga qaytish uchun ENTER bosing")

    elif choice == "0":
        clear()
        print("👋 Dastur yopildi")
        break

    else:
        input("❌ Noto‘g‘ri tanlov! ENTER bosing")
