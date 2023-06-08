from django.shortcuts import render
from django.http import HttpResponse
import requests, json
from mysite import models           # 匯入 mysite 資料夾底下 models.py 中所有的類別
from bs4 import BeautifulSoup

import random   #匯入亂數模組

def index(request):
    myname = "王欽弘"
    return render(request, "index.html", locals())

def all_data(request):
    url = "https://opendata.hccg.gov.tw/OpenDataFileHit.ashx?ID=48DEDBDAC3A31FC6&u=77DFE16E459DFCE3F5CEA2F931E333F7E23D5729EF83D5F20744125E844FB27044F9892E6F09372518441B3BB84260426ADE242A57DFB9E8C9A50C50134F4F47"
    r = requests.get(url)
    data = json.loads(r.text)
    msg = ""
    msg = "<h2>" + data["updated_at"] + "</h2><br>"
    bicycle_data = data["retVal"]
    msg = msg + "<table><tr><td>站名</td><td>自行車數量</td></tr>"
    for item in bicycle_data:
        msg = msg + "<tr bgcolor=#ccffcc><td>{}</td><td>{}/{}</td></tr>".format(
            item['sna'].split("_")[1], 
            item['sbi'], 
            item['tot'])
    msg = msg + "</table>"
    return HttpResponse(msg)

def filtered_data(request):
    # 先刪除所有的舊資料
    models.HBicycleData.objects.all().delete()
    # 先把所有的資料放到資料庫中，比照all_data()中的程式碼
    url = "https://opendata.hccg.gov.tw/OpenDataFileHit.ashx?ID=48DEDBDAC3A31FC6&u=77DFE16E459DFCE3F5CEA2F931E333F7E23D5729EF83D5F20744125E844FB27044F9892E6F09372518441B3BB84260426ADE242A57DFB9E8C9A50C50134F4F47"
    r = requests.get(url)
    data = json.loads(r.text)
    bicycle_data = data["retVal"]
    for item in bicycle_data:
        new_record = models.HBicycleData(
            sna = item['sna'].split("_")[1],
            sbi = int(item['sbi']),
            tot = int(item['tot']))
        new_record.save()
    # 從資料表裡面過濾出我們想要的資料
    data = models.HBicycleData.objects.filter(sbi__gte=10)
    return render(request, "filter.html", locals())

def nkustnews(request):
    data = models.NKUSTnews.objects.all()
    return render(request, "nkustnews.html", locals())

def phonelist(request, id=-1):
    if id==-1:
        data = models.PhoneModel.objects.all()
    else:
        maker = models.PhoneMaker.objects.get(id=id)         #找一個用get
        data = models.PhoneModel.objects.filter(maker=maker) #找好多個，用filter
    return render(request, "phonelist.html", locals())

def chart(request):
    data = models.PhoneModel.objects.all()
    return render(request, "chart.html", locals())

def stock300list(request):
    data = models.StockInfo.objects.filter(price__gte=300).order_by('-price')
    numbers = len(data)
    return render(request, "stocklist.html", locals())

def oil_price_update(request):
    models.Oil.objects.all().delete()
    r = requests.get(
        "https://vipmbr.cpc.com.tw/CPCSTN/ListPriceWebService.asmx/getCPCMainProdListPrice_XML").text.splitlines()
    for i in range(len(r)):
        if r[i]== "    <產品名稱>98無鉛汽油</產品名稱>":
            price_line = r[i+5]
            #    <參考牌價>28.5</參考牌價>

            models.Oil(
                name="98無鉛汽油",
                price=float(price_line[10:-7])
            ).save()
        elif r[i] == "    <產品名稱>95無鉛汽油</產品名稱>":
            price_line = r[i+5]
            #    <參考牌價>28.5</參考牌價>

            models.Oil(
                name="95無鉛汽油",
                price=float(price_line[10:-7])
            ).save()
        elif r[i] == "    <產品名稱>92無鉛汽油</產品名稱>":
            price_line = r[i+5]
            #    <參考牌價>28.5</參考牌價>

            models.Oil(
                name="95無鉛汽油",
                price=float(price_line[10:-7])
            ).save()
        elif r[i] == "    <產品名稱>超級柴油</產品名稱>":
            models.Oil(
                name="超級柴油",
                price=float(price_line[10:-7])
            ).save()
    return HttpResponse("<h1>Updated oil price</h1>")

def oil_price(request):
    data = models.Oil.objects.all()
    numbers = len(data)
    return render(request, "oil_price.html", locals())
