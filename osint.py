import asyncio
import aiohttp
import time

TIMEOUT = aiohttp.ClientTimeout(total=7)
HEADERS = {"User-Agent": "Mozilla/5.0 (Async OSINT Scanner)"}

PLATFORMS = {
    # SOCIAL
    "Instagram": "https://www.instagram.com/{}",
    "Facebook": "https://www.facebook.com/{}",
    "TikTok": "https://www.tiktok.com/@{}",
    "Twitter": "https://twitter.com/{}",
    "Threads": "https://www.threads.net/@{}",
    "Snapchat": "https://www.snapchat.com/add/{}",
    "Pinterest": "https://www.pinterest.com/{}",
    "OK": "https://ok.ru/{}",
    "VK": "https://vk.com/{}",
    "Tumblr": "https://{}.tumblr.com",
    "Weibo": "https://weibo.com/{}",
    "Mastodon": "https://mastodon.social/@{}",
    "Hive": "https://hive.blog/@{}",
    "Plurk": "https://www.plurk.com/{}",
    "MeWe": "https://mewe.com/{}",

    # VIDEO
    "YouTube": "https://www.youtube.com/@{}",
    "Twitch": "https://www.twitch.tv/{}",
    "Kick": "https://kick.com/{}",
    "Dailymotion": "https://www.dailymotion.com/{}",
    "Vimeo": "https://vimeo.com/{}",
    "Rumble": "https://rumble.com/user/{}",
    "Bilibili": "https://space.bilibili.com/{}",
    "Odysee": "https://odysee.com/@{}",
    "PeerTube": "https://peertube.tv/accounts/{}",

    # DEV
    "GitHub": "https://github.com/{}",
    "GitLab": "https://gitlab.com/{}",
    "Bitbucket": "https://bitbucket.org/{}",
    "SourceForge": "https://sourceforge.net/u/{}/profile",
    "HackerRank": "https://www.hackerrank.com/{}",
    "Codeforces": "https://codeforces.com/profile/{}",
    "LeetCode": "https://leetcode.com/{}",
    "Replit": "https://replit.com/@{}",
    "CodePen": "https://codepen.io/{}",
    "StackOverflow": "https://stackoverflow.com/users/{}",
    "Dev.to": "https://dev.to/{}",
    "Hashnode": "https://hashnode.com/@{}",
    "IndieHackers": "https://www.indiehackers.com/{}",
    "AngelList": "https://angel.co/u/{}",
    "Glitch": "https://glitch.com/@{}",    

    # MUSIC
    "SoundCloud": "https://soundcloud.com/{}",
    "Spotify": "https://open.spotify.com/user/{}",
    "Bandcamp": "https://bandcamp.com/{}",
    "Mixcloud": "https://www.mixcloud.com/{}",
    "Audiomack": "https://audiomack.com/{}",
    "LastFM": "https://www.last.fm/user/{}",
    "ReverbNation": "https://www.reverbnation.com/{}",

    # GAMES
    "Steam": "https://steamcommunity.com/id/{}",
    "Xbox": "https://account.xbox.com/profile?gamertag={}",
    "PlayStation": "https://psnprofiles.com/{}",
    "EpicGames": "https://store.epicgames.com/u/{}",
    "Ubisoft": "https://www.ubisoft.com/en-us/profile/{}",
    "Origin": "https://www.ea.com/users/{}",
    "BattleNet": "https://battle.net/account/management/{}",
    "Roblox": "https://www.roblox.com/user.aspx?username={}",
    "Chess": "https://www.chess.com/member/{}",
    "Lichess": "https://lichess.org/@/{}",    

    # DESIGN
    "Dribbble": "https://dribbble.com/{}",
    "Behance": "https://www.behance.net/{}",
    "ArtStation": "https://www.artstation.com/{}",
    "Unsplash": "https://unsplash.com/@{}",
    "500px": "https://500px.com/{}",
    "DeviantArt": "https://{}.deviantart.com",
    "Flickr": "https://www.flickr.com/people/{}",    

    # BLOG
    "Reddit": "https://www.reddit.com/user/{}",
    "Medium": "https://medium.com/@{}",
    "WordPress": "https://{}.wordpress.com",
    "Blogger": "https://{}.blogspot.com",
    "Quora": "https://www.quora.com/profile/{}",
    "Hackernoon": "https://hackernoon.com/u/{}",    

    # MONEY
    "KoFi": "https://ko-fi.com/{}",
    "BuyMeACoffee": "https://www.buymeacoffee.com/{}",
    "Patreon": "https://www.patreon.com/{}",
    "PayPal": "https://www.paypal.me/{}",
    "Venmo": "https://venmo.com/{}",
    "OpenCollective": "https://opencollective.com/{}",    

    # CRYPTO
    "OpenSea": "https://opensea.io/{}",
    "Rarible": "https://rarible.com/{}",
    "Foundation": "https://foundation.app/@{}",
    "Zora": "https://zora.co/{}",
    "Etherscan": "https://etherscan.io/address/{}",    

    # BIO
    "Linktree": "https://linktr.ee/{}",
    "Bento": "https://bento.me/{}",
    "Carrd": "https://{}.carrd.co",
    "Notion": "https://www.notion.so/{}",
    "Trello": "https://trello.com/{}",
    "AboutMe": "https://about.me/{}",    

    # OTHER
    "Keybase": "https://keybase.io/{}",
    "Pastebin": "https://pastebin.com/u/{}",
    "Slideshare": "https://slideshare.net/{}",
    "Goodreads": "https://www.goodreads.com/{}",
    "Gravatar": "https://en.gravatar.com/{}"
}

async def check(session, name, url):
    try:
        async with session.get(url, allow_redirects=True) as r:
            if r.status in [200, 301, 302]:
                return name, "FOUND"
            elif r.status in [401, 403]:
                return name, "RESTRICTED"
            else:
                return name, "NOT_FOUND"
    except:
        return name, "NOT_FOUND"

async def main():
    username = input(" Username: ").strip()
    start = time.time()

    async with aiohttp.ClientSession(headers=HEADERS, timeout=TIMEOUT) as session:
        tasks = [
            check(session, name, url.format(username))
            for name, url in PLATFORMS.items()
        ]
        results = await asyncio.gather(*tasks)

    for name, status in results:
        icon = "" if status == "FOUND" else "" if status == "RESTRICTED" else ""
        print(f"{icon} {status:11} | {name}")

    print(f"\n Vaqt: {round(time.time() - start, 2)}s")

asyncio.run(main())
