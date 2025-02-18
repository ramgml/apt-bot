FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    LANG=ru_RU.UTF-8 \
    LANGUAGE=ru_RU:ru \
    LC_ALL=ru_RU.UTF-8 \
    TERM=xterm-256color

WORKDIR /app

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install --upgrade pip && pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY src/ /app/
