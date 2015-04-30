"""
Django settings for kormushka project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = [os.path.join(BASE_DIR, 'templates')]


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yb)#+xq$4=h(8ixv!aff2+&*2)(5fs)5538wpb1cy5ts5on$zu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',
    'loginsys',
    #'django_jenkins',
)

JENKINS_TASKS = ('django_jenkins.tasks.run_pylint',
                 'django_jenkins.tasks.run_pep8',
                 'django_jenkins.tasks.run_pyflakes',
                 'django_jenkins.tasks.with_coverage',
                 'django_jenkins.tasks.django_tests',)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware'#для определение локали пользователя.
)

ROOT_URLCONF = 'kormushka.urls'

WSGI_APPLICATION = 'kormushka.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'kormushkadb.sqlite3'),
    }
}

#изменяем модуль аутентификации на тот, что возвращает экземпляра CustomUser вместо User.
AUTHENTICATION_BACKENDS = (
    #'loginsys.auth_backends.CustomUserModelBackend',
    'loginsys.auth_backends.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',   #комментируем эту строку, для запрета доступа superuser's
)

#изменяем класс для работы с пользователями
CUSTOM_USER_MODEL = 'loginsys.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = '/opt/korm_dev/kormushka/kormushka/static/'

AUTH_INFORMATION = { 'LDAP': {
    'USERNAME_SEARCH_FILTER': '(uid={})',
    'USERGROUP_SEARCH_FILTER': '(gidNumber={})',
    'HOST': "ldap://188.166.9.61",
    'PORT': 389,
    'BASE_DN': 'ou=people,dc=test,dc=com',
    'GROUPS_DN': 'ou=groups,dc=test,dc=com'
}}