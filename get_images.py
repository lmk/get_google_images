import urllib2
import os
from bs4 import BeautifulSoup
import sys, json

DIR= "./Pictures/"
query= "korea actor face"
query=  '+'.join(query.split())  #this will make the query terminator+3
url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"
header={'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36"
}
req= urllib2.Request(url,headers=header)
soup= urllib2.urlopen(req)
soup= BeautifulSoup(soup)

ActualImages=[]# contains the link for Large original images, type of  image
for a in soup.find_all("div",{"class":"rg_meta"}):
    link , Type =json.loads(a.text)["ou"]  ,json.loads(a.text)["ity"]
    ActualImages.append((link,Type))
 
for i , (img , Type) in enumerate( ActualImages):
    try:
        req = urllib2.Request(img, headers={'User-Agent' : header})
        raw_img = urllib2.urlopen(req).read()
        if not os.path.exists(DIR):
            os.mkdir(DIR)
        cntr = len([i for i in os.listdir(DIR) if query in i]) + 1
        print cntr
        if len(Type)==0:
            f = open(DIR + query + "_"+ str(cntr)+".jpg", 'wb')
        else:
            f = open(DIR + query + "_"+ str(cntr)+"."+Type, 'wb')
        f.write(raw_img)
        f.close()
    except Exception as e:
        print "could not load : "+img
        print e
