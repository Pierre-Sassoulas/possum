#FROM django:1.9-python3
FROM python:3.4-slim
MAINTAINER S. Bonnegent <sebastien.bonnegent@gmail.com>

#USER root

# on ajoute une arborescence
# mount -o bind /home/bonnegent/Projets/dsi-django /home/bonnegent/Projets/dockers/centos-python27-dsi/dsi-django
#ADD dsi-django /opt/dsi-django

# pour se positionner dans un repertoire
# WORKDIR /opt/dsi-django

# RUN au moment du build
#RUN yum -y install gcc python-devel libjpeg-turbo-devel zlib-devel openldap-devel unzip && \
#    cd /opt/dsi-django && NOENV="yes" ./make update && \
#    yum clean all

# USER 1001

# Set the default CMD to print the usage of the language image
#CMD $STI_SCRIPTS_PATH/usage
#CMD /bin/bash


RUN apt-get update && apt-get install -y \
        gcc \
        gettext \
        postgresql-client libpq-dev \
        sqlite3 \
        libcups2-dev \
        cups-client \
    --no-install-recommends && apt-get clean

#ENV DJANGO_VERSION 1.9.2
#RUN pip install psycopg2 django=="$DJANGO_VERSION"

ADD . /app/
WORKDIR /app

ENV NOENV yes
RUN ./make update && ./make load_demo

EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
