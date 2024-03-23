# Distance education system

## Установка зависимостей

```bash
poetry install
```

## Миграции

```bash
poetry run py ./manage.py makemigrations
poetry run py ./manage.py migrate
```

## Запуск проекта

```bash
poetry run py ./manage.py runserver
```

Сервер запускается на http://127.0.0.1:8000/

## Запуск тестов

```bash
poetry run py ./manage.py test
```

## Swagger

Документация API запускается на http://127.0.0.1:8000/api/docs