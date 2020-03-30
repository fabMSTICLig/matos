import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=True

# Web acces protections
ALLOWED_HOSTS = ['localhost']
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8080',
    'http://localhost:8081'
]
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:8080',
    'http://localhost:8081'
]

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
EMAIL_HOST = 'smtp.orange.fr'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'clement.lesaulnier@orange.fr'
EMAIL_HOST_PASSWORD = 'artisansFab0120'
EMAIL_USE_TLS = True
EMAIL_TIMEOUT=10
# FacManager Email settings
# Email which sends notification mails
EMAIL_SENDER = 'clement.lesaulnier@orange.fr'
# Emails which received notification mails
EMAIL_ADMIN = ['clement.lesaulnier@orange.fr',]

if DEBUG == True:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    STATIC_ROOT = ''
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "./static"),
    ]

