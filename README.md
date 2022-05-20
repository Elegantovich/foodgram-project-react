# foodgram-project-react


![Status](https://github.com/elegantovich/foodgram-project-react/actions/workflows/main.yml/badge.svg)


Приложение развернуто по адресу http://51.250.23.61/

## Описание

Проект **foodgram-project-react** собирает любителей кулинарии на одной платформе. Можно добавлять и обмениваться рецептами любимых блюд.

## Стек технологий

- asgiref==3.5.0
- autopep8==1.6.0
- certifi==2021.10.8
- cffi==1.15.0
- charset-normalizer==2.0.12
- coreapi==2.3.3
- coreschema==0.0.4
- cryptography==36.0.1
- defusedxml==0.7.1
- Django==2.2.19
- django-colorfield==0.6.3
- django-extra-fields==3.0.2
- django-filter==21.1
- django-rest-framework==0.1.0
- django-templated-mail==1.1.1
- djangorestframework==3.13.1
- djoser==2.1.0
- flake8==4.0.1
- idna==3.3
- importlib-metadata==1.7.0
- itypes==1.2.0
- Jinja2==3.0.3
- MarkupSafe==2.1.0
- mccabe==0.6.1
- oauthlib==3.2.0
- Pillow==9.0.1
- psycopg2-binary==2.8.6
- pycodestyle==2.8.0
- pycparser==2.21
- pyflakes==2.4.0
- PyJWT==2.3.0
- python-dotenv==0.19.2
- python3-openid==3.2.0
- pytz==2021.3
- reportlab==3.6.9
- requests==2.27.1
- requests-oauthlib==1.3.1
- six==1.16.0
- social-auth-app-django==4.0.0
- social-auth-core==4.2.0
- sqlparse==0.4.2
- toml==0.10.2
- typing_extensions==4.1.1
- uritemplate==4.1.1
- urllib3==1.26.8
- zipp==3.7.0
- gunicorn==20.0.4
## Установка на локальном компьютере
Эти инструкции помогут вам создать копию проекта и запустить ее на локальном компьютере для целей разработки и тестирования.

### Установка Docker
Установите Docker, используя инструкции с официального сайта:
- для [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- для [Linux](https://docs.docker.com/engine/install/ubuntu/). Отдельно потребуется установть [Docker Compose](https://docs.docker.com/compose/install/)

### Запуск проекта.
Склонируйте этот репозиторий в текущую папку
```
git clone https://github.com/Elegantovich/API_Blog/
```
Перейдите в папку 'infra'
```
cd infra
```
Создайте файл `.env` командой
```
touch .env
```
и добавьте в него переменные окружения для работы с базой данных:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432 
DJANGO_KEY='your_key'
```
Запустите docker-compose:
```
docker-compose up -d --build
```
Накатите миграции:
```
docker-compose exec web python manage.py migrate
```
Создайте суперпользователя:
```
docker-compose exec web python manage.py createsuperuser
```
Соберите статику в единую папку:
```
docker-compose exec web python manage.py collectstatic --no-input
```
Создать пользователя можно через джанго-админгу
```
http//localhost/admin/
```

## Деплой на удаленный сервер
Для запуска проекта на удаленном сервере необходимо:
```
- создать переменные окружения в разделе `secrets` настроек текущего репозитория:
```
DHANGO_KEY - ключ джанго проекта

LIST_HOST - allow_host
SSH_KEY
### данные по postgresql
```
POSTGRES_PASSWORD
POSTGRES_USER
DB_ENGINE
DB_HOST
DB_NAME
DB_PORT
HOST
```
### данные по докеру
```
DOCKER_PASSWORD
DOCKER_USERNAME
```
### данные по телеграмму
```
TELEGRAM_TO
TELEGRAM_TOKEN 
```

### После каждого обновления репозитория (`git push`) будет происходить:
1. Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest из репозитория foodgram-project-react
2. Сборка и доставка докер-образов на Docker Hub.
3. Автоматический деплой.
4. Отправка уведомления в Telegram.


### Авторы

[Хачатрян Максим](https://github.com/Elegantovich)<br>

