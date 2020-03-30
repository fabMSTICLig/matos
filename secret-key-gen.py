"""
Two things are wrong with Django's default `SECRET_KEY` system:
1. It is not random but pseudo-random
2. It saves and displays the SECRET_KEY in `settings.py`
This snippet
1. uses `SystemRandom()` instead to generate a random key
2. saves a local `secret.txt`
The result is a random and safely hidden `SECRET_KEY`.
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_FILE = os.path.join(BASE_DIR, 'config/secret-key.txt')

def setEncryptionKey() :
    try:
        import random
        SECRET_KEY = ''.join([random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)') for i in range(50)])
        with open(SECRET_FILE, 'w') as secret:
            secret.write(SECRET_KEY)
            print(SECRET_KEY)
            secret.close()
    except IOError:
        Exception('Please create a %s file with random characters \
        to generate your secret key!' % SECRET_FILE)

try:
    SECRET_KEY

except NameError:
    try:
        with open(SECRET_FILE, 'r') as file:
            data = file.read().replace('\n', '')
            if (data == ''):
                setEncryptionKey()
        SECRET_KEY = open(SECRET_FILE).read().strip()

    except IOError:
        setEncryptionKey()

