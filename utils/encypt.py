import hashlib
from django.conf import settings


def md5(string):
    """ MS5加密"""
    hash_objects = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    hash_objects.update(string.encode('utf-8'))
    return hash_objects.hexdigest()
