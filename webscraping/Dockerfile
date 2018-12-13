FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN apk update \
    && apk add build-base python3-dev libffi-dev libxml2-dev libxslt-dev openssl-dev \
    && pip3 install -r requirements.txt \
    && apk del build-base

CMD python src/main.py
