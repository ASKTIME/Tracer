import os
import sys
import django

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Tracer.settings")
django.setup()  #

from WEB import models

models.UserInfo.objects.create(username='name1', email='name1@qq.com',
                               mobile_phone='13144446666', password='12345678')
