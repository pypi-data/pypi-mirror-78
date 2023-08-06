import time
import zxing
from socket import*
from email.mime.text import MIMEText
from random import*
import smtplib
import requests
import json
import platform
import sys
import urllib.request ,re,os
import time
from re import*
import requests
from urllib.request import*
import json
def baidubaike(text):
    html=urllib.request.urlopen("http://gop.asunc.cn/baike.html").read().decode("utf-8")
    url=html+urllib.parse.quote(text)
    html=urllib.request.urlopen(url).read().decode("utf-8")
    par = '(<meta name="description" content=")(.*?)(">)'
    try:
        data = re.search(par,html).group(2)
        return data
    except:
        return -1
def translate(string):
    data = {'doctype': 'json','type': 'AUTO','i':string}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    result = result['translateResult'][0][0]["tgt"]
    return result
def getweather(province,city):
    tf=0
    data = {'doctype': 'json','type': 'AUTO','i':province}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    province = result['translateResult'][0][0]["tgt"]
    data = {'doctype': 'json','type': 'AUTO','i':city}
    url = "http://fanyi.youdao.com/translate"
    r = requests.get(url,params=data)
    result = r.json()
    city = result['translateResult'][0][0]["tgt"]
    try:
        wurl="https://tianqi.moji.com/weather/china/"+province+'/'+city
        html = urllib.request.urlopen(wurl).read().decode("utf-8")
        par = '(<meta name="description" content=")(.*?)(">)'
        data = re.search(par, html).group(2)
        data = data.replace(",", "，").replace("。", "，").replace("墨迹天气建议您", "爱搜天气助手建议您")
        return data
    except:
        return -1

def get_news():
    now = time.strftime("%Y-%m-%d", time.localtime())
    print(now,"最新新闻资讯,转载于人民日报。\n")
    now = time.strftime("%Y%m%d", time.localtime())
    now1 = time.strftime("%Y-%m/%d", time.localtime())
    print("今日新闻资讯:")
    for i in range(1,10):
        try:
            url="http://paper.people.com.cn/rmrb/html/"+now1+"/nw.D110000renmrb_"+now+"_3-0"+str(i)+".htm"
            html=urlopen(url).read().decode("utf-8")
            html=html.replace("<br>","")
            html=html.replace("&nbsp;","")
            html=html.replace("<P>","")
            html=html.replace("</P>","")
            a1=html.index("<title>")+len("<title>")
            b1=html.index("</title>")
            a=html.index("<!--enpcontent-->")+19
            b=html.index("<!--/enpcontent-->")
            print(i,".",end="")
            while a1<b1:
                print(html[a1],end="")
                a1+=1
            print("\n")
        except:
            last=i-1
            break
    try:
        number=int(input("您需要的看点:"))
    except:
        return -1
    if number>last or number<1:
        return -1
    url="http://paper.people.com.cn/rmrb/html/"+now1+"/nw.D110000renmrb_"+now+"_3-0"+str(number)+".htm"
    html=urlopen(url).read().decode("utf-8")
    html=html.replace("<P>","")
    html=html.replace("</P>","")
    html=html.replace("<br>","")
    html=html.replace("&nbsp;","")
    a1=html.index("<title>")+len("<title>")
    b1=html.index("</title>")
    a=html.index("<!--enpcontent-->")+19
    b=html.index("<!--/enpcontent-->")
    print("标题:")
    while a1<b1:
        print(html[a1],end="")
        a1+=1
    print("\033[33m")
    while a1<b1:
        print(html[a1],end="")
        a1+=1
    print("\033[0m")
    print("\n内容:")
    print("\033[44m",end="  ")
    while a<b:
        print(html[a],end="")
        a+=1
    print("\033[0m")

def printf(text,ts=0.1):
    text=str(text)
    for i in text:
        print(i,end='')
        time.sleep(ts)
#def cleardevice():
    #import sys
    #sys.stdout.write("\033[2J\033[00H")

def find_lib(libname):
    try:
        url='http://127.0.0.1:55820/package/search?name='+libname
        a=json.loads(urlopen(url).read().decode())
        if a['data']['option'][0]['state']=='not_installed':
            return False
        elif a['data']['option'][0]['state']=='installed':
            return True
    except:
        return -1
