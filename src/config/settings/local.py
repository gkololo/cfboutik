from .base import *

# Configuration pour le développement local
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Base de données SQLite pour le développement
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}