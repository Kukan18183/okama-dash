FROM python:3.9.7-slim as build

WORKDIR /var/www/app

COPY ./requirements.txt ./requirements.txt

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev python3-dev && \
    pip install --no-cache-dir -r ./requirements.txt

COPY . .

EXPOSE 8050

CMD python run_gunicorn.py