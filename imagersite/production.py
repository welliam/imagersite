import os
from imagersite.settings import BASE_DIR


DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['ec2-54-191-95-187.us-west-2.compute.amazonaws.com']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'imagersite'
EMAIL_HOST_PASSWORD = 'keyerrorenus'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'imagersite@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
