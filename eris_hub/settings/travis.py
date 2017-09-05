from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eris_test',
        'USER': 'travis',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}