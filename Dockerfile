FROM python:3.4-slim
MAINTAINER S. Bonnegent <sebastien.bonnegent@gmail.com>

RUN apt-get update && apt-get install -y \
        gcc \
        gettext \
        postgresql-client libpq-dev \
        sqlite3 \
        libcups2-dev \
        cups-client \
    --no-install-recommends && apt-get clean

ADD . /app/
WORKDIR /app

ENV NOENV yes
RUN ./make update && ./make load_demo

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
