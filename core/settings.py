import os
import dj_database_url
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-xq+w!wsa62r1(6h_f#_#vy5j)2a7tbgm7_m$$4uyxrkyjfo1d)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# AJUSTE PARA O NGROK: Permite rodar local e aceita qualquer subdomínio gerado pelo Ngrok (.ngrok-free.app)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.render.com', '*']


# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'corsheaders',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'reservas',
    'relatorios',
    'rest_framework',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # <- ADICIONADO PARA OS ESTÁTICOS NO RENDER
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.wsgi.application'


# POSTGRESQL local
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'anexaracj',
#        'USER': 'mah_admin',
#        'PASSWORD': 'acelerando',
#        'HOST': 'localhost',      # Quando for para o Windows, se o banco estiver na mesma máquina, continua 'localhost'
#        'PORT': '5432',
#    }
#}


# POSTGRESQL plataforma do RENDER.com
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://axra_casajoao_user:NoDoR9DJg8tvhSs75tHXB3A7WsXdBD5z@dpg-d90u1alaeets73ee0feg-a/axra_casajoao',
        conn_max_age=600
    )
}


# Password validation
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


# Internationalization
LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'reservas', 'static'),
]


# Pasta onde o Django vai reunir todos os arquivos estáticos em produção para o Render ler
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração extra para o Whitenoise compactar os arquivos estáticos com eficiência
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# configurações para django interface
X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

# Libera o acesso da API para qualquer origem (essencial para testes locais e com Ngrok)
CORS_ALLOW_ALL_ORIGINS = True