from pathlib import Path
from decouple import config
import dj_database_url
import os
from datetime import timedelta
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# امنیت و محیط
# ========================
SECRET_KEY = config('SECRET_KEY', default='replace-this-key-for-dev')
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS', 
    default='https://marjanrezaei-store.onrender.com',
    cast=lambda v: [s.strip() for s in v.split(',')]
)

# ========================
# اپلیکیشن‌ها
# ========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mail_templated',
    'django_celery_beat',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'parler',
    
    'website',
    'dashboard',
    'accounts',
    'shop',
    'cart',
    'order',
    'payment',
    'review',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'cart.middleware.CartMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# ========================
# دیتابیس
# ========================
# Get DATABASE_URL from environment or use local default
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres")

# Configure Django DATABASES
DATABASES = {
    "default": dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        ssl_require=os.getenv("ENV") == "production"  # Enable SSL only if using remote DB
    )
}
# ========================
# رمز عبور
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ========================
# بین‌المللی سازی
# ========================
LANGUAGE_CODE = 'fa'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('fa', _('فارسی')), 
    ('en', _('English')),
    ('ar', _('العربية')),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

PARLER_DEFAULT_LANGUAGE_CODE = 'fa'
PARLER_LANGUAGES = {
    None: (
        {'code': 'fa'},
        {'code': 'en'},
        {'code': 'ar'},
    ),
    'default': {
        'fallbacks': ['fa'],  
        'hide_untranslated': False,
    }
}
# ========================
# استاتیک و مدیا
# ========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ========================
# کاربر سفارشی
# ========================
AUTH_USER_MODEL = 'accounts.User'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# ========================
# ایمیل
# ========================
if DEBUG:
    EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
    DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = "smtp.gmail.com"
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")        
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD") 
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)


FRONTEND_URL = config('FRONTEND_URL', default='http://127.0.0.1:8000' if DEBUG else 'https://marjanrezaei-store.onrender.com')
# ========================
# Liara object storage
# ========================
LIARA_OBJECT_STORAGE = {
    'bucket_name': 'marjan',
    'aws_access_key_id': config('LIARA_ACCESS_KEY', default=''),
    'aws_secret_access_key': config('LIARA_SECRET_KEY', default=''),
}

# ========================
# Celery
# ========================
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default="redis://127.0.0.1:6379/0")
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default="redis://127.0.0.1:6379/0")
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ========================
# پرداخت
# ========================
MERCHANT_ID = config('MERCHANT_ID', default='your-merchant-id')
SANDBOX_MODE = config('SANDBOX_MODE', default=True, cast=bool)

# ========================
# DRF + JWT
# ========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
