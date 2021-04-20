from django.conf.urls import url, include
from app01 import views
app_name = 'app01'
urlpatterns = [
    url(r'^send_sms/', views.send_sms), # "app01:register"
    url(r'^register/', views.register),
]
