# Flower Bot

В данном проекте реализован Telegram бот 
для заказа цветов.
В качестве ORM системы и админки используется Django

## Как установить

Python3 должен быть установлен версии ~3.11.* и выше.
Используйте `pip` для установки зависимостей:
```python
$ pip install -r requirements.txt
```

## Настройка проекта

Во первых, вам понадобится Telegram бот.
Создать его можно через [@BotFather](https://t.me/BotFather).

После успешного создания бота, вам понадобится его токен.

Бот токен выглядит так: 

- `1234567890:XXXxx0Xxx-xxxX0xXXxXxx0X0XX0XXXXxXx`. 

Во вторых, вам понабится файл .env.

```python
BOT_TOKEN = 'Ваш токен'
DJANGO_SECRET_KEY = 'django-insecure-br'
DJANGO_DEBUG = True
ALLOWED_HOSTS = .localhost,127.0.0.1,[::1],.fvds.ru
CROSS_OR = http://*.fvds.ru
ADMIN_ID = ''
COURIER_ID = 'id курьера в Telegram'
FLORIST_ID = 'id флориста в Telegram'
SITE_URL = 'http://customer.fast-vds.ru'
```

## Команды запуска

Делаем стартовую миграцию:
```python
$ py backend/manage.py makemigrations
```
Запускаем миграции в БД:
```python
$ py backend/manage.py migrate
```
Создаём админа:
```python
$ py backend/manage.py createsuperuser
```
Команда для заполнения базы данных:
```python
$ py backend/manage.py fill_db
```

Запускаем Django (локально):
```python
$ py backend/manage.py runserver
```
Запускаем бота в другом терминале:
```python
$ py backend/manage.py runbot
```

Для деплоя проекта рекомендуем ознакомиться с [данной](https://docs.djangoproject.com/en/5.0/howto/deployment/) статьей.

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).