import string
from fake_useragent import UserAgent
import requests
import random
from threading import Thread
import time
from twocaptcha import TwoCaptcha

solver = TwoCaptcha('TwoCaptchaKey')
THREAD_NUMBER = 100
out = open('cookies.txt', 'a') #save cookies here
ua = UserAgent()
threads = []

proxies = {
    "http": "YOUR_PROXY_HERE",
    "https": "YOUR_PROXY_HERE"
}


def get_cookies():
    while True:
        s = requests.session()
        s.headers = {}
        headers = {
            "Host": "news.ycombinator.com",
            "Cache-Control": "max-age=0",
            "Sec-Ch-Ua": '"Chromium";v="105", "Not)A;Brand";v="8"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Linux",
            "Upgrade-Insecure-Requests": "1",
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
        password = random.choices(string.ascii_letters + string.digits, k=8)
        data = {
            "creating": "t",
            "acct": ''.join(random.choices(string.ascii_letters + string.digits, k=12)),
            "pw": ''.join(password)
        }

        try:
            res = s.post('https://news.ycombinator.com/login', data=data, allow_redirects=False, proxies=proxies,
                         headers=headers)
            if res.status_code == 302:
                cookie = res.headers["Set-Cookie"].split(';')[0]
                print('Created account: ' + cookie)
                out.write(cookie + "\n")
            else:
                data["g-recaptcha-response"] = solver.recaptcha(sitekey="6LfPsiITAAAAAKTxriyPED2gw1_7HxeR4GC7N3HH",
                                                                url="https://news.ycombinator.com/login")["code"]
                res = s.post('https://news.ycombinator.com/login', data=data, allow_redirects=False, proxies=proxies,
                             headers=headers)
                if res.status_code == 302:
                    cookie = res.next.headers["Cookie"].split('user=')[-1]
                    print('Created account: ' + cookie)
                    out.write("user=" + cookie + "\n")
                else:
                    print('There was an error creating an account')
        except:
            continue

for i in range(THREAD_NUMBER):
    threads.append(Thread(target=get_cookies, args=[]))
    threads[i].start()

while 1:
    try:
        time.sleep(0.1)
    except KeyboardInterrupt:
        out.close()
        break
