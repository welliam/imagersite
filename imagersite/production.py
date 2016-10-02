import os
from imagersite.settings import BASE_DIR


DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['ec2-54-191-95-187.us-west-2.compute.amazonaws.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
