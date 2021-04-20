from django.conf.urls import url, include
from django.contrib import admin
from WEB.views import account
app_name = 'WEB'
urlpatterns = [
    url(r'^register/$', account.register, name='register'),
]
