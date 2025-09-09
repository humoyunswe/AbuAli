import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIRS = BASE_DIR / 'templates'

SECRET_KEY = 'SECRET_KEY', 'django-insecure-ln$5^(*$ffb)$9c%9m@pf&pq!d%7d)(!fcf@^@b*dt7pf4(y&w'
DEBUG = True
ALLOWED_HOSTS = ['*','127.0.0.1', '.vercel.app', 'localhost', 'abuali.uz', 'www.abuali.uz']

AUTH_USER_MODEL = 'accounts.CustomUser'

# Default apps for development
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # your apps
    'about_us',
    'accounts',
    'articles',
    'comments',
    'likes',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'widget_tweaks',
    'projects',
    'candidate',
]



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'uzbek_code.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIRS, ],
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

WSGI_APPLICATION = 'uzbek_code.wsgi.app'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'neondb',  # из конца URL
        'USER': 'neondb_owner',  # имя пользователя
        'PASSWORD': 'npg_QLCjF5Or3JSX',  # пароль
        'HOST': 'ep-rapid-tree-ad6uxfic-pooler.c-2.us-east-1.aws.neon.tech',  # хост
        'PORT': '5432',  # порт
        'OPTIONS': {
            'sslmode': 'require',  # для Neon обязательно
        },
    }
}


# Production database configuration (PostgreSQL)
if os.getenv('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.parse(os.getenv('DATABASE_URL'))

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru'
LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian'),
    ('uz', 'Uzbek'),
)
LOCALE_PATHS = (BASE_DIR / 'locale',)

TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# --- Static & Media Files ---
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Use StaticFilesStorage for development to avoid CSS loading issues
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# --- CKEditor ---
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js'

# Use CDN for CKEditor instead of local files
CKEDITOR_BASEPATH = "https://cdn.ckeditor.com/4.22.1/standard/"
CKEDITOR_UPLOAD_PREFIX = "https://cdn.ckeditor.com/4.22.1/standard/"

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
        'height': 400,
        'width': '100%',
        'removePlugins': 'stylesheetparser',
        'allowedContent': True,
    },
}

# --- Email (dev only) ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# --- Auth redirects ---
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Cache (optional) ---
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 3600,
    }
}

# --- Vercel specific settings ---
if os.getenv('VERCEL') or os.getenv('VERCEL_URL'):
    # Minimal apps without heavy packages
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # Only essential apps
        'about_us',
        'accounts',
        'articles',
        'projects',
        'candidate',
        'widget_tweaks',  # lightweight
    ]
    
    # Use simple static files without CKEditor
    STATIC_URL = '/static/'
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    
    # Disable debug on Vercel
    DEBUG = False
    
    # Force HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Database connection optimization for serverless
    if 'default' in DATABASES:
        DATABASES['default']['CONN_MAX_AGE'] = 0
    
    # Reduce logging
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'WARNING',
            },
        },
    }

