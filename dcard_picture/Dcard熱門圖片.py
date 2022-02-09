#藉由首頁取得所有文章的URL
import requests
from bs4 import BeautifulSoup
import json
import time

test = open("spider/popular/log.txt","w",encoding='UTF-8')


p = requests.Session()
url=requests.get("https://www.dcard.tw/f/sex")
soup = BeautifulSoup(url.text,"html.parser")
sel = soup.select("div.sc-1db29sy-0.cKDgas a.tgn9uw-3.bJQtxM")
a=[]
print("=====================儲存文章網址=====================")
test.write("=====================儲存文章網址=====================\n")
for s in sel:
    a.append(s["href"])

for k in range(0,10):
    print("==================增加 {} 次 30篇文章==================".format(k))
    test.write("==================增加 {} 次 30篇文章==================\n".format(k)) 
    post_data={
        "before":a[-1][9:18],
        "limit":"30",
        "popular":"true",
    }
    r = p.get("https://www.dcard.tw/_api/forums/sex/posts",params=post_data, headers = { "Referer": "https://www.dcard.tw/", "User-Agent": "Mozilla/5.0" })
    data2 = json.loads(r.text)
    for u in range(len(data2)):
        Temporary_url = "/f/sex/p/"+ str(data2[u]["id"]) + "-" + str(data2[u]["title"].replace(" ","-"))
        a.append(Temporary_url)
    time.sleep(1)

time.sleep(1)
j=0 #為了印頁數
q=0 #為了印張數
print("=====================開始抓取圖片=====================")
test.write("=====================開始抓取圖片=====================\n")
for i in a[2:]:
    url = "https://www.dcard.tw"+i
    j+=1
    print ("第",j,"篇的URL為:"+url)
    #file.write("temperature is {} wet is {}%\n".format(temperature, humidity))
    test.write("第 {} 頁的URL為: {} \n".format(j,url))
    url=requests.get(url)
    soup = BeautifulSoup(url.text,"html.parser")
    sel_jpg = soup.select("div.inetk9-0.ccaBir img")
    for c in sel_jpg:
        q+=1
        print("第",q,"張:",c["src"])
        test.write("%\n""第 {} 張: {} \n".format(q,c["src"])) 
        pic=requests.get(c["src"])
        img2 = pic.content
        pic_out = open("spider/popular/"+str(q)+".png",'wb')
        pic_out.write(img2)
        pic_out.close()

test.close()
print("爬蟲結束")