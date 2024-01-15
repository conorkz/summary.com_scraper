from bs4 import BeautifulSoup
import re
import os
import requests
from datetime import datetime
import pytz
from http.cookies import SimpleCookie
dir = r'YOUR_DIR'
roi = 'no info on the website'
x = 1
rawdata = "YOUR_COOKIE_AFTER_YOU_LOGGED_IN"
cookie = SimpleCookie()
cookie.load(rawdata)
cookies = {k: v.value for k, v in cookie.items()}
session = requests.Session()
session.cookies.update(cookies)
while True:
    link = f'https://www.summary.com/book-summaries/page/{x}/'
    response = requests.get(link, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, "html.parser")
    print(f'\nPAGE: {link}\n')
    x+=1
    if not soup.select_one('li .thumbnail-link'):
        break
    for g in soup.select('li .thumbnail-link'):
        url = g['href']
        respons = session.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        sorpa = BeautifulSoup(respons.content, "html.parser")
        print(f'LINK: {url}')
        title = sorpa.select_one('.top-title').text
        if sorpa.select_one('.sub-title'):
            subtitle = sorpa.select_one('.sub-title').text
        else:
            subtitle = roi
        if sorpa.select_one('.author'):
            author = re.sub(r"\s+", " ", sorpa.select_one('.author').text.replace('By','').strip())
        else:
            author = roi
        if sorpa.select_one('.reading-time'):
            time = re.sub(r"\s+", " ", sorpa.select_one('.reading-time').text.strip())
        else:
            time = roi
        if sorpa.select_one('.summary-image.wp-post-image'):
            img = sorpa.select_one('.summary-image.wp-post-image')['src']
        else:
            img = roi
        if sorpa.find(class_='cont-wrap'):
            kl = []
            for j in sorpa.find(class_='cont-wrap').find_all(['p','h6','li']):
                kl.append(j.text.strip())
            desc = "\n\n".join(kl)
        else:
            desc = roi
        if sorpa.select_one('.back-link'):
            amazon = sorpa.select_one('.back-link')['href']
        else:
            amazon = roi
        berlin = datetime.now(pytz.timezone('Europe/Berlin')).strftime('%Y-%m-%d %H:%M:%S %Z')
        bf = re.sub(r"[^\w\s]", "", title)
        file_name = os.path.join(dir, f"{bf}.txt")
        suffix = 1
        while os.path.exists(file_name):
            file_name = os.path.join(dir, f"{bf} ({suffix}).txt")
            suffix += 1
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(f"Link: {url}\n")
            file.write(f"Title: {title}\n")
            file.write(f"Subtitle: {subtitle}\n")
            file.write(f"Author: {author}\n")
            file.write(f"Time to read and listen: {time}\n")
            file.write(f"Book cover: {img}\n")
            file.write(f"Amazon link: {amazon}\n")
            file.write(f"Berlin time: {berlin}\n\n")
            file.write(f"Description: {desc}\n\n")
            if sorpa.select_one('.btn-blue.ico-book'):
                lnk = sorpa.select_one('.btn-blue.ico-book')['href']
                respon = session.get(lnk, headers={'User-Agent': 'Mozilla/5.0'})
                sorp = BeautifulSoup(respon.content, "html.parser")
                for g in sorp.find(class_='file-content').find_all(['p','h1','h2','h4','h3','li','h5']):
                    file.write(g.text.strip() + '\n\n')
