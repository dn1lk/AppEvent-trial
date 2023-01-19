from pathlib import Path

# Зададим корневой путь приложения
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'STRONG_SECRET_KEY'  # задаём своё значение


DEBUG = True  # в продакшн не выходим, свои адреса не задаём
ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'main.apps.PostsConfig',  # регистрируем приложение
]


ROOT_URLCONF = 'main.urls'  # регистрируем ссылки


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "name",  # задаём из настроек базы данных
        'USER': "user",  # задаём из настроек базы данных
        'PASSWORD': "password",  # задаём из настроек базы данных
        'HOST': "localhost",  # задаём из настроек базы данных
        'PORT': "3306",  # задаём из настроек базы данных
    }
}


TIME_ZONE = 'Europe/Moscow'
USE_TZ = True
