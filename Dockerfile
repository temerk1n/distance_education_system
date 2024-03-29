FROM python:3.10.4

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app/

COPY . /usr/src/app/

RUN pip3 install poetry

RUN poetry install

RUN poetry run python manage.py makemigrations

RUN poetry run python manage.py migrate