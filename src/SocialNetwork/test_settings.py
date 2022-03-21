from .settings import *

DJANGO_DEBUG = True
ENVIRONMENT = "test"
SECRET_KEY = 'kkkkjjjjoooo999'

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
