FROM python:3.6-alpine AS build
COPY . /app
WORKDIR /app
RUN apk update \
    && apk add build-base python3-dev libffi-dev libxml2-dev libxslt-dev openssl-dev \
    && pip3 install -r requirements.txt

FROM python:3.6-alpine
COPY --from=build /usr/local/lib/python3.6/site-packages/ /usr/local/lib/python3.6/site-packages/
COPY . /app
WORKDIR . /app
CMD ["python" "-m" "scrapy" "crawl" "hardverapro"]
