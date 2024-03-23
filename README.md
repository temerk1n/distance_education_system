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
Перед запуском сервера необходимо провести миграцию базы данных (инструкция выше).

Сервер запускается на http://127.0.0.1:8000/

## Запуск тестов

Для запуска Unit-тестов используйте следующую команду:

```bash
poetry run py ./manage.py test assessment/tests/unit_tests
```

Для запуска компонентных тестов используйте:

```bash
poetry run py ./manage.py test assessment/tests/component_tests
```

## Swagger

Документация API запускается на http://127.0.0.1:8000/api/docs