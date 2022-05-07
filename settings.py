import os

BASE_DIR = os.path.dirname(__file__)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, "todolist.sqlite3"),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
}

INSTALLED_APPS = [
    # 'django.contrib.messages',
    # 'django.contrib.staticfiles',
    'rest_framework',
    # 'corsheaders',
    'dal.data_store.MyDjangoAppConfig',

    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # https://docs.djangoproject.com/en/4.0/howto/static-files/
]

CORS_ORIGIN_ALLOW_ALL = True

MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

ROOT_URLCONF = 'urls'

STATIC_URL = 'static/'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=!aono@k%00zpt^o&%k#p03yx5&&o&nmkx$4r!bft7))3b1lsy'

# === panedrone:
# https://docs.djangoproject.com/en/4.0/howto/static-files/
# (staticfiles.E002) The STATICFILES_DIRS setting should not contain the STATIC_ROOT setting.
STATICFILES_DIRS = [
    # BASE_DIR /
    "static",
]

# STATIC_ROOT = 'static/'

TEMPLATES = [  # === panedrone: generated defaults
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        # https://stackoverflow.com/questions/1123898/django-static-page
        # === panedrone:
        'DIRS': [BASE_DIR], #[os.path.join(BASE_DIR, 'static')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DEBUG = True
ALLOWED_HOSTS = ['*']
# DEBUG = False
