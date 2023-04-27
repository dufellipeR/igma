FROM python:3.10.9-alpine3.17

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

WORKDIR /app

RUN pip install --upgrade pip

ADD ./requirements.txt /app/

RUN pip install -r requirements.txt

ADD . /app/

CMD python manage.py runserver 0.0.0.0:8000
