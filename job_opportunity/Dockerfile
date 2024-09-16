FROM python:3.11.4-alpine

RUN apk add --no-cache nodejs npm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYCODE 1

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./package.json /usr/src/app/package.json
RUN npm install

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

COPY . /usr/src/app/

ENTRYPOINT ["/bin/sh", "/usr/src/app/entrypoint.sh"]