import requests
import random
from fake_useragent import UserAgent
from threading import Thread

inf = open('cookies.txt', 'r') #each line is a cookie in the form of user=username&hash
cookies = []
line = inf.readline()
while line:
    cookies.append(line.strip('\n'))
    line = inf.readline()
random.shuffle(cookies)
ua = UserAgent()
THREAD_NUMBER = 1
threads = []

proxies = {
    "http": "YOUR_PROXY_HERE",
    "https": "YOUR_PROXY_HERE"
}

id = 123456789 #change with post id
class Info:
    upvotes = 0

def upvote():
    for cookie in cookies:
        try:
            res = requests.get(f'https://news.ycombinator.com/item?id={id}', headers={"Cookie": cookie})
            auth = res.text.split("how=up&amp;auth=")[1].split('&amp;')[0]
            s = requests.session()
            s.headers = {}
            headers = {
                "Host": "news.ycombinator.com",
                "Cache-Control": "max-age=0",
                "Sec-Ch-Ua": '"Chromium";v="105", "Not)A;Brand";v="8"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": "Linux",
                "Upgrade-Insecure-Requests": "1",
                "Cookie": cookie,
                "Origin": "https://news.ycombinator.com",
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": str(ua.chrome),
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Referer": "https://news.ycombinator.com/",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "close"
            }
            res = s.get(f'https://news.ycombinator.com/vote?id={id}&how=up&auth={auth}&goto=item?id={id}&js=t',
                        proxies=proxies, headers=headers, allow_redirects=False, timeout=10)
            if res.status_code == 302 and res.headers["Location"] == "ok":
                Info.upvotes += 1
                print("Current upvotes: " + str(Info.upvotes))
            else:
                if res.is_redirect:
                    print("Location: " + res.headers["Location"])
                print("Couldn't upvote.")
        except:
            print('There was an error with cookie: ' + cookie)
            continue

for i in range(THREAD_NUMBER):
    threads.append(Thread(target=upvote, args=[]))
    threads[i].start()
