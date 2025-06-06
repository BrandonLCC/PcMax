"""
Django settings for PcMax project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-n=z97k^er)p_a#6%e&y(@z=ub3)f$9!czlg91b%=v8gkaskmyn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap5',
    'store',
    'rest_framework',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PcMax.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'PcMax.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'UTC'

USE_I10N = True

USE_I18N = True

USE_TZ = True

LANGUAGE =[
    ('es', 'español'),
    ('en', 'English'),
    
    ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'
LOGIN_REDIRECT_URL = 'home' 
LOGOUT_REDIRECT_URL = 'home'  
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de Jazzmin

JAZZMIN_SETTINGS = {

  "site_title": "Pcmax", # Título del sitio que aparece en la pestaña del navegador.

  "site_header": "Panel de Administrador", # Encabezado del sitio en el panel de administración.

  #titulo de login al regresar a la pagina de login
    "site_login": "Iniciar Sesión",
   
  "site_brand": "Panel de Administrador", # Marca o nombre del sitio que aparece en la barra de navegación.

    #logo de la tienda
    "site_logo": "images/logo-empresa.jpg",

  

  "welcome_sign": "Bienvenido ", # Mensaje de bienvenida que aparece en la página de inicio de sesión.

  "search_model": "auth.User", # Modelo utilizado para la búsqueda global en el panel de administración.

  "show_sidebar": True, # Muestra la barra lateral del menú.

  "navigation_expanded": True, # Expande la navegación por defecto.

  "order_with_respect_to": ["auth", "books", "book.author", "book.book"], # Orden de las aplicaciones y modelos en el menú.

  "icons": { # Iconos para las aplicaciones y modelos específicos.

    "auth": "fas fa-users-cog", # Icono para la aplicación de autenticación.

    "auth.user": "fas fa-user", # Icono para el modelo de usuario.

    "auth.Group": "fas fa-users", # Icono para el modelo de grupos.

  },

  "default_icon_parents": "fas fa-chevron-circle-right", # Icono por defecto para las aplicaciones principales.

  "default_icon_children": "fas fa-circle", # Icono por defecto para los modelos dentro de las aplicaciones.

}


import os
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'store/static'),  # Caarpeta para archivos estáticos
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Carpeta para archivos de medios (subidos)

