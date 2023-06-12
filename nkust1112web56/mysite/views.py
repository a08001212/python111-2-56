from django.shortcuts import render
from django.http import HttpResponse
import requests, json
from mysite import models           # 匯入 mysite 資料夾底下 models.py 中所有的類別
from bs4 import BeautifulSoup
import time, threading

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

def oil_price_update():
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
            models.Oil(
                name="92無鉛汽油",
                price=float(price_line[10:-7])
            ).save()
        elif r[i] == "    <產品名稱>超級柴油</產品名稱>":
            price_line = r[i+5]
            models.Oil(
                name="超級柴油",
                price=float(price_line[10:-7])
            ).save()
    # return HttpResponse("<h1>Updated oil price</h1>")

def oil_price(request):
    data = models.Oil.objects.all()
    numbers = len(data)
    return render(request, "oil_price.html", locals())



def update_codeforces():
    urls = "https://codeforces.com/ratings/page/{}"
    models.Codeforces_data.objects.all().delete()

    for page in range(1, 600):
        url = urls.format(page)
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        # sel = "#pageptlist > div > div > div > div.d-txt > div.mtitle > a"
        table = soup.find_all("table")[5]
        score = 0
        ranking = 0
        name = ""
        for row in table.find_all("tr"):
            count = 0
            for elem in row.find_all('td'):
                if count > 4:
                    continue

                if count % 4 == 0:
                    ranking = int(elem.text.strip())
                elif count % 4 == 1:
                    name = elem.text.strip()
                elif count % 4 == 3:
                    score = int(elem.text.strip())
                    if score < 2400:
                        return HttpResponse("<h1>updated data.</h1>")
                    models.Codeforces_data(
                        name = name,
                        score = score,
                        ranking = ranking
                    ).save()
                count += 1

        time.sleep(3)  # 這是每一頁讀取之間的間隔，絕對不能省略
        print("page:{}".format(page))

def codeforces_red_name(request):
    data = models.Codeforces_data.objects.all()
    size = len(data)
    return render(request, "codeforces_red_name.html", locals())

def update_cpe():
    models.Cpe.objects.all().delete()
    def get_cpe_average(url):
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        ul = soup.find_all("ul")[-1]
        # print(len(ul.find_all('li')[-1].text.strip()))
        return float(ul.find_all('li')[-1].text.strip()[7:])

    # models.NKUSTnews.objects.all().delete()
    urls = "https://cpe.cse.nsysu.edu.tw/history.php"
    html = requests.get(urls).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "mtable"})
    for row in table.find_all("tr")[1:]:
        data = row.find_all('td')
        date = data[0].text.strip()
        # print(date[:4])
        # date
        # data[0].text.strip()

        if int(data[0].text.strip()[0:4]) <= 2013:
            break

        d = data[1].find_all('a', href=True)
        if len(d) > 1:
            url = d[0]['href']
            avg = get_cpe_average(url)
            models.Cpe(
                name = data[0].text.strip(),
                average = avg
            ).save()

    # return HttpResponse("<h1>update sessusful</h1>")


def cpe(request):
    data = models.Cpe.objects.all()[::-1]
    size = len(data)
    return render(request, "cpe.html", locals())

def update_all_data(request):
    def update():
        oil_price_update()
        print("oil price update sessusful.")
        # request.get("127.0.0.1:8000/update_oil_price/")
        update_codeforces()
        print("codeforces update sessusful.")
        # request.get("127.0.0.1:8000/update_codeforces/")
        update_cpe()
        # request.get("127.0.0.1:8000/update_cpe")
        print("update cpe data.\nUpdated all data.")
    th = threading.Thread(target = update)
    th.start()
    return HttpResponse("<h1>updating data</h1>")