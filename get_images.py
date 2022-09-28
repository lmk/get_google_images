#-*- coding: utf-8 -*-
import os
from bs4 import BeautifulSoup
import requests
import validators

DIR = "./Pictures/"

QUERY = "안구정화"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
}

if not os.path.exists(DIR):
    os.mkdir(DIR)

QUERY =  '+'.join(QUERY.split())
url ="https://www.google.co.in/search?q="+QUERY+"&source=lnms&tbm=isch"

res = requests.get(url, timeout=3, headers=HEADERS)

if res.status_code != 200:
    print("Error: ", res.status_code)
    quit()

soup = BeautifulSoup(res.text, "html.parser")

for h1 in soup.find_all("h1"):
    if h1.text == "Search results":
        soup = h1.findNext("div")
        break

i = 1
for img in soup.find_all("img"):
    if "src" in img.attrs:
        url = img.attrs["src"]
    elif "data-src" in img.attrs:
        url = img.attrs["data-src"]
    
    if not validators.url(url):
        continue

    try:
        res = requests.get(url, timeout=3, headers=HEADERS)
        if res.status_code != 200:
            continue

        resType = ""
        if "Content-Type" in res.headers:
            resType = res.headers["Content-Type"]

        imgType = ""
        for t in ["jpeg", "svg", "png", "gif", "bmp"]:
            if t in resType:
                imgType = t
                break

        if imgType == "":
            continue

        fn = QUERY + "_{0:03d}.".format(i) + imgType
        print("download. ", fn)
        open(DIR + "/" + fn, "wb").write(res.content)
        i = i + 1

    except Exception as e:
        print("could not load : " + img)
 