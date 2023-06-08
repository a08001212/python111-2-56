import requests
import time
from bs4 import BeautifulSoup
import os
# import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nkust1112web56.settings')
# django.setup()
# from mysite import models

# models.NKUSTnews.objects.all().delete()
urls = "https://codeforces.com/ratings/page/{}"
for page in range(1, 2):
    url = urls.format(page)
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    # sel = "#pageptlist > div > div > div > div.d-txt > div.mtitle > a"
    sel = "#pageContent.content-with-sidebar > div.datatable.ratingsDatatable > div > table > tbody > tbody > tr > td.dark > a.rated-user user-red"
    table = soup.find_all("table")[5]
    rows = []
    count = 0
    score = 0
    ranking = 0
    name = ""
    for row in table.find_all("tr"):
        for elem in row.find_all('td'):
            if count % 4 == 0:
                ranking int(elem.text.strip())
            elif count % 4 == 1:
                name = elem.text.strip()
            elif count % 4 == 3:
                score = int(elem.text.strip)
            count += 1
    # for tag in tags:
    #     print(count)
    #     print("=" * 10)
    #     count += 1
    #     print(tag)

    # titles = soup.select(sel)
    # for title in titles:
    #     print(title.text)
        # new_rec = models.NKUSTnews(title=title.text.strip())
        # new_rec.save()
    time.sleep(3)                 #這是每一頁讀取之間的間隔，絕對不能省略
    print("page:{}".format(page))
print("Done!")

