import asyncio
import aiohttp
import time
from dataclasses import dataclass
from typing import Tuple, Dict, List
from enum import Enum

# Rang kodlari (ANSI)
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'

# Iconlar
class Icons:
    FOUND = f"{Colors.GREEN}✓{Colors.RESET}"
    NOT_FOUND = f"{Colors.RED}✗{Colors.RESET}"
    RESTRICTED = f"{Colors.YELLOW}⚠{Colors.RESET}"
    LOADING = f"{Colors.CYAN}⌛{Colors.RESET}"

# Status enumeration
class Status(Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    RESTRICTED = "RESTRICTED"

@dataclass
class PlatformResult:
    name: str
    url: str
    status: Status
    response_time: float = 0.0

TIMEOUT = aiohttp.ClientTimeout(total=7)
HEADERS = {"User-Agent": "Mozilla/5.0 (Async OSINT Scanner/1.0)"}

PLATFORMS = {
    # Kategoriyalar
    "SOCIAL MEDIA": {
        "Instagram": "https://www.instagram.com/{}",
        "Facebook": "https://www.facebook.com/{}",
        "TikTok": "https://www.tiktok.com/@{}",
        "Twitter": "https://twitter.com/{}",
        "Threads": "https://www.threads.net/@{}",
        "Snapchat": "https://www.snapchat.com/add/{}",
        "Pinterest": "https://www.pinterest.com/{}",
        "VK": "https://vk.com/{}",
        "Weibo": "https://weibo.com/{}",
        "Mastodon": "https://mastodon.social/@{}",
    },
    
    "VIDEO PLATFORMS": {
        "YouTube": "https://www.youtube.com/@{}",
        "Twitch": "https://www.twitch.tv/{}",
        "Kick": "https://kick.com/{}",
        "Bilibili": "https://space.bilibili.com/{}",
        "Vimeo": "https://vimeo.com/{}",
        "Rumble": "https://rumble.com/user/{}",
    },
    
    "DEVELOPER": {
        "GitHub": "https://github.com/{}",
        "GitLab": "https://gitlab.com/{}",
        "StackOverflow": "https://stackoverflow.com/users/{}",
        "LeetCode": "https://leetcode.com/{}",
        "HackerRank": "https://www.hackerrank.com/{}",
        "CodePen": "https://codepen.io/{}",
        "Dev.to": "https://dev.to/{}",
    },
    
    "GAMING": {
        "Steam": "https://steamcommunity.com/id/{}",
        "Roblox": "https://www.roblox.com/user.aspx?username={}",
        "EpicGames": "https://store.epicgames.com/u/{}",
        "Xbox": "https://account.xbox.com/profile?gamertag={}",
        "Chess.com": "https://www.chess.com/member/{}",
    },
    
    "DESIGN & ART": {
        "Behance": "https://www.behance.net/{}",
        "Dribbble": "https://dribbble.com/{}",
        "ArtStation": "https://www.artstation.com/{}",
        "DeviantArt": "https://{}.deviantart.com",
        "Unsplash": "https://unsplash.com/@{}",
    },
    
    "BLOGGING": {
        "Reddit": "https://www.reddit.com/user/{}",
        "Medium": "https://medium.com/@{}",
        "Quora": "https://www.quora.com/profile/{}",
        "Blogger": "https://{}.blogspot.com",
    },
    
    "FINANCE": {
        "Patreon": "https://www.patreon.com/{}",
        "Ko-Fi": "https://ko-fi.com/{}",
        "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
        "PayPal": "https://www.paypal.me/{}",
        "OpenSea": "https://opensea.io/{}",
    },
    
    "OTHER": {
        "Spotify": "https://open.spotify.com/user/{}",
        "SoundCloud": "https://soundcloud.com/{}",
        "Linktree": "https://linktr.ee/{}",
        "Keybase": "https://keybase.io/{}",
        "Goodreads": "https://www.goodreads.com/{}",
    }
}

def print_banner():
    banner = f"""
{Colors.CYAN}{'='*60}
{Colors.BOLD}{Colors.MAGENTA}          ASYNC OSINT SCANNER{Colors.RESET}
{Colors.CYAN}{'='*60}{Colors.RESET}
{Colors.GRAY}Version: 2.0 | By: Python Developer{Colors.RESET}
{Colors.CYAN}{'-'*60}{Colors.RESET}
    """
    print(banner)

def print_summary(results: List[PlatformResult], duration: float):
    found = sum(1 for r in results if r.status == Status.FOUND)
    restricted = sum(1 for r in results if r.status == Status.RESTRICTED)
    not_found = sum(1 for r in results if r.status == Status.NOT_FOUND)
    
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"{Colors.BOLD}SCAN SUMMARY:{Colors.RESET}")
    print(f"{Colors.CYAN}{'-'*60}{Colors.RESET}")
    print(f"{Colors.GREEN}✓ Found:        {found:3d}{Colors.RESET}")
    print(f"{Colors.YELLOW}⚠ Restricted:   {restricted:3d}{Colors.RESET}")
    print(f"{Colors.RED}✗ Not Found:    {not_found:3d}{Colors.RESET}")
    print(f"{Colors.CYAN}─"*60)
    print(f"{Colors.BOLD}Total:          {len(results):3d}{Colors.RESET}")
    print(f"{Colors.GRAY}Time:           {duration:.2f}s{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*60}{Colors.RESET}\n")
    
    if found > 0:
        print(f"{Colors.GREEN}{Colors.BOLD}FOUND PROFILES:{Colors.RESET}")
        print(f"{Colors.GREEN}{'─'*60}{Colors.RESET}")
        for result in results:
            if result.status == Status.FOUND:
                print(f"  {Icons.FOUND} {result.name:<20} → {Colors.BLUE}{result.url}{Colors.RESET}")

async def check_platform(session: aiohttp.ClientSession, name: str, url: str) -> PlatformResult:
    """Check single platform for username"""
    start_time = time.time()
    
    try:
        async with session.get(url, allow_redirects=True) as response:
            elapsed = time.time() - start_time
            
            if response.status in [200, 301, 302]:
                return PlatformResult(name, url, Status.FOUND, elapsed)
            elif response.status in [401, 403, 429]:
                return PlatformResult(name, url, Status.RESTRICTED, elapsed)
            else:
                return PlatformResult(name, url, Status.NOT_FOUND, elapsed)
                
    except (aiohttp.ClientError, asyncio.TimeoutError):
        return PlatformResult(name, url, Status.NOT_FOUND, time.time() - start_time)

def print_category_results(category: str, results: List[PlatformResult]):
    """Print results for a specific category"""
    print(f"\n{Colors.BOLD}{Colors.WHITE}[ {category} ]{Colors.RESET}")
    print(f"{Colors.GRAY}{'─'*60}{Colors.RESET}")
    
    for result in results:
        if result.status == Status.FOUND:
            icon = Icons.FOUND
            color = Colors.GREEN
            status_text = "FOUND"
        elif result.status == Status.RESTRICTED:
            icon = Icons.RESTRICTED
            color = Colors.YELLOW
            status_text = "RESTRICTED"
        else:
            icon = Icons.NOT_FOUND
            color = Colors.RED
            status_text = "NOT FOUND"
        
        # Format qator
        print(f"  {icon} {color}{status_text:<12}{Colors.RESET} │ {result.name:<25} {Colors.GRAY}[{result.response_time:.2f}s]{Colors.RESET}")

async def main():
    print_banner()
    
    # Username input
    print(f"{Colors.BOLD}Enter username to scan:{Colors.RESET}")
    username = input(f"{Colors.CYAN}└─>{Colors.WHITE} ").strip()
    
    if not username:
        print(f"{Colors.RED}Error: Username required!{Colors.RESET}")
        return
    
    print(f"\n{Colors.YELLOW}Scanning for '{username}'...{Colors.RESET}")
    print(f"{Colors.GRAY}{'─'*60}{Colors.RESET}")
    
    start_time = time.time()
    all_results = []
    
    async with aiohttp.ClientSession(headers=HEADERS, timeout=TIMEOUT) as session:
        # Har bir kategoriya uchun parallel tekshirish
        for category_name, platforms in PLATFORMS.items():
            tasks = []
            category_results = []
            
            # Har bir platformaga task yaratish
            for name, url_template in platforms.items():
                url = url_template.format(username)
                task = check_platform(session, name, url)
                tasks.append(task)
            
            # Natijalarni olish
            category_results = await asyncio.gather(*tasks)
            
            # Natijalarni chop etish
            print_category_results(category_name, category_results)
            
            # Barcha natijalarga qo'shish
            all_results.extend(category_results)
            
            # Qisqa pauza (rate limiting uchun)
            await asyncio.sleep(0.1)
    
    # Umumiy natijalarni chiqarish
    duration = time.time() - start_time
    print_summary(all_results, duration)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Scan interrupted by user{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
