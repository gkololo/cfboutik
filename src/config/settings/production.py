from .base import *

# Configuration pour la production
DEBUG = False

ALLOWED_HOSTS = ['ton-domaine.com', 'www.ton-domaine.com']  # À changer plus tard

# Base de données PostgreSQL pour la production (exemple)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'boutique_db',
#         'USER': 'username',
#         'PASSWORD': 'password',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

# Sécurité renforcée
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True