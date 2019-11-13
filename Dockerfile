FROM python:3.7

LABEL maintainer="Scientific Software Platform"

ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get -y install --upgrade \
      # bash \
      # locales \
      # locales-all \
      # wget \
      # apache2 \
      # apache2-dev \
      default-mysql-client \
      default-libmysqlclient-dev \
      libcurl4-openssl-dev \
      libssl-dev \
      libffi-dev \
      libxml2-dev \
      libxslt1-dev
      # libapache2-mod-wsgi-py3 \
      # python3-opencv

# ENV LC_ALL en_US.UTF-8
# ENV LANG en_US.UTF-8
# ENV LANGUAGE en_US.UTF-8

# Requirements are installed here to ensure they will be cached.
RUN pip install pipenv
COPY ./Pipfile* /app/
COPY ./libraries/pyforms-web /app/libraries/pyforms-web
COPY ./plugins/confirm-users-app /app/plugins/confirm-users-app
COPY ./plugins/notifications-central /app/plugins/notifications-central
COPY ./plugins/fishdb /app/plugins/fishdb
COPY ./plugins/flydb /app/plugins/flydb
COPY ./plugins/rodentdb /app/plugins/rodentdb
RUN cd /app && \
    pipenv install --deploy --ignore-pipfile && \
    cd /

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

## Add the wait script to the image
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.6.0/wait /wait
RUN chmod +x /wait

WORKDIR /app

EXPOSE 80 443

ENTRYPOINT ["/entrypoint"]
