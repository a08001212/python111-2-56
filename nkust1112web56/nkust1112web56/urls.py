from django.contrib import admin
from django.urls import path
from mysite import views   # 引入views.py中所有的函式

urlpatterns = [
    path('', views.index),      # 設定執行首頁顯示的功能由index函式負責
    path('nkustnews/', views.nkustnews),
    path('phonelist/', views.phonelist),  #列出所有的新款手機
    path('phonelist/maker/<int:id>/', views.phonelist),  #列出指定廠牌的所有手機
    path('stock300list/', views.stock300list),  #列出所有股價超過300元的公司
    path('chart/', views.chart),
    path('all/', views.all_data),         #顯示所有的站台資訊
    path('filter/', views.filtered_data), #只顯示超過5台可用自行車的站台資訊
    path('admin/', admin.site.urls),
    path('update_oil_price/', views.oil_price_update),
    path('oil_price/', views.oil_price),
    path('update_codeforces/', views.update_codeforces),
    path('codeforces_red_name/', views.codeforces_red_name),
    path('update_cpe/', views.update_cpe),
    path('cpe/', views.cpe),
]
