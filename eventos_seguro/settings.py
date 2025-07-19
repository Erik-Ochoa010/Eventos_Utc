from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-@x4&rl-rxsp8ir1@k#f($p))qq9zrp3j@m2&9rq4n+$l)k&0#_'

# Variable para controlar si estás en entorno local de desarrollo
LOCAL_DEV = True  # 👈 CAMBIA a False cuando lo subas a producción

# Activa DEBUG solo en desarrollo
DEBUG = LOCAL_DEV

# Dominios o IPs permitidos
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'tu-dominio.com']  # Cambia 'tu-dominio.com'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eventos',
    'axes',  # django-axes para protección contra fuerza bruta
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'axes.middleware.AxesMiddleware',  # Debe ir antes de AuthenticationMiddleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eventos_seguro.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'eventos' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'eventos_seguro.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eventos_utc',
        'USER': 'root',
        'PASSWORD': 'sigurd',
        'HOST': '127.0.0.1',
        'PORT': '3307',
    }
}

AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # backend recomendado para django-axes >= 5.0
    'django.contrib.auth.backends.ModelBackend',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'eventos' / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ------ CONFIGURACIONES DE SEGURIDAD ------
if LOCAL_DEV:
    # Configuración para desarrollo local (sin HTTPS)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    # Configuración para producción (con HTTPS)
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Prevención de ataques comunes
X_FRAME_OPTIONS = 'DENY'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# django-axes settings (solo estas dos)
AXES_FAILURE_LIMIT = 5  # Bloquea después de 5 intentos fallidos
AXES_COOLOFF_TIME = 1   # Tiempo de bloqueo en horas

# NOTA: Se eliminaron estas configuraciones obsoletas que generan warnings:
# AXES_ONLY_USER_FAILURES
# AXES_LOCK_OUT_BY_COMBINATION_USER_AND_IP
# AXES_USE_USER_AGENT
