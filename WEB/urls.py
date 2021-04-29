from django.conf.urls import url, include
from django.contrib import admin
from WEB.views import account
from WEB.views import home

# app_name = 'WEB'
urlpatterns = [
    url(r'^register/$', account.register, name='register'),
    url(r'^send/sms/$', account.send_sms, name='send_sms'),
    url(r'^login/sms/$', account.login_sms, name='login_sms'),
    url(r'^login/$', account.login, name='login'),
    url(r'^logout/$', account.logout, name='logout'),
    url(r'^index/$', home.index, name='index'),
    url(r'^image/code/$', account.image_code, name='image_code'),
]
