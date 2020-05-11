import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True

# Web acces protections
ALLOWED_HOSTS = ['localhost']

CSRF_COOKIE_DOMAIN="localhost"

if DEBUG == False :
    SESSION_COOKIE_SECURE=True
    CSRF_COOKIE_SECURE=True
    USE_X_FORWARDED_HOST=True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CAS settings
CAS_SERVER_URL = 'https://cas-simsu.grenet.fr/login'
CAS_VERSION = '3'

# Email settings
# https://docs.djangoproject.com/en/2.2/topics/email/
EMAIL_HOST = 'smtp.mail.fr'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'USERMAIL'
EMAIL_HOST_PASSWORD = 'PASSWORD'
EMAIL_USE_TLS = True
EMAIL_TIMEOUT=10
# FacManager Email settings
# Email which sends notification mails
EMAIL_SENDER = 'USERMAIL'
# Emails which received notification mails
EMAIL_ADMIN = ['USERMAIL',]

if DEBUG == True:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_ROOT = ''
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "./static"),
    ]

