from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ¡No olvides cambiar esta clave por una secreta en producción y NO subirla a GitHub!
SECRET_KEY = 'django-insecure-@x4&rl-rxsp8ir1@k#f($p))qq9zrp3j@m2&9rq4n+$l)k&0#_'

# Variable para controlar entorno (True = desarrollo local, False = producción)
LOCAL_DEV = True  # Cambiar a False cuando despliegues en Render o en producción

# Debug activo solo en desarrollo
DEBUG = LOCAL_DEV

# Dominios permitidos (agrega aquí tus dominios reales)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'tu-dominio.com', 'eventos-utc.onrender.com']

# Aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'eventos',
    'axes',  # Protección contra ataques de fuerza bruta
]

# Middleware, axes debe ir antes que AuthenticationMiddleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'axes.middleware.AxesMiddleware',  # Protege login con django-axes
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'eventos_seguro.urls'

# Plantillas HTML
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

# Configuración de base de datos (verifica que la config sea válida en Render)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'eventos_utc',
        'USER': 'root',
        'PASSWORD': 'sigurd',
        'HOST': '127.0.0.1',  # En Render puede cambiar (base de datos externa)
        'PORT': '3307',
    }
}

# Backends de autenticación (axes primero para control de intentos fallidos)
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internacionalización
LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'America/Mexico_City'
USE_I18N = True
USE_TZ = True

# Archivos estáticos y media
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'eventos' / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Configuraciones de seguridad según entorno ---
if LOCAL_DEV:
    # Desarrollo local (sin HTTPS)
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
else:
    # Producción (HTTPS activado)
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 3600  # 1 hora, puedes aumentar después
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Prevención de ataques comunes
X_FRAME_OPTIONS = 'DENY'               # Evita que el sitio se cargue en iframes externos
SECURE_BROWSER_XSS_FILTER = True       # Activa filtro XSS del navegador
SECURE_CONTENT_TYPE_NOSNIFF = True     # Evita que el navegador interprete incorrectamente contenido

# Configuración django-axes para protección de fuerza bruta
AXES_FAILURE_LIMIT = 5  # Número de intentos fallidos antes de bloquear
AXES_COOLOFF_TIME = 1   # Tiempo en horas que dura el bloqueo

