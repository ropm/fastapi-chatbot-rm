FROM pytorch/pytorch:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update
RUN apt-get install gcc python-dev libpq-dev -y


COPY requirements.txt .
RUN pip install -r requirements.txt

ADD start-reload.sh /app

RUN chmod +x /app/start-reload.sh

COPY . .