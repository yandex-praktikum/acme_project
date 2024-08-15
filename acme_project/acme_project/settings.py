from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-m&$lzdzkutvrbr5vt=jpm)7#g7cken_tk%($ty+w902n7wb#=e'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    # Когда проект будет опубликован и станет доступен для пользователей,
    # в этот список нужно будет добавить и адреса домена, где он будет размещён,
    # например 'acme.not' и 'www.acme.not'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'birthday.apps.BirthdayConfig',
    'pages.apps.PagesConfig',
    'django_bootstrap5',
    # Регистрируем новое приложение в проекте:
    # обязательно ниже, чем django.contrib.staticfiles.
    'debug_toolbar',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'acme_project.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (TEMPLATES_DIR,),
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

WSGI_APPLICATION = 'acme_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'

# Подключаем бэкенд filebased.EmailBackend:
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# Указываем директорию, в которую будут сохраняться файлы писем:
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'
# После логина будем перенаправлять пользователя на главную страницу — homepage
LOGIN_REDIRECT_URL = 'pages:homepage'
# Адрес страницы логина можно указать в настройках проекта, в константе LOGIN_URL
LOGIN_URL = 'login'
# Имя view-функции, обрабатывающей ошибку 403, указывается в settings.py, в константе CSRF_FAILURE_VIEW
CSRF_FAILURE_VIEW = 'core.views.csrf_failure'
# Добавьте в settings.py эту константу, чтобы DjDT знал,
# запросы с каких IP он должен обрабатывать.
INTERNAL_IPS = [
    '127.0.0.1',
]
