FROM python:3.8

RUN apt-get update && \
    pip install --upgrade pip

WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r /app/requirements.txt

COPY . /app

EXPOSE 9000

CMD ./manage.py migrate && \
    ./manage.py collectstatic --noinput && \
    gunicorn quizes.wsgi -b 0.0.0.0:9000