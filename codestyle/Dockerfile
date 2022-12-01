FROM python:3.9.7-alpine
RUN apk add --no-cache --virtual .build-deps \
  gcc \
  musl-dev

VOLUME /code
WORKDIR /codestyle

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

ENTRYPOINT ["./entrypoint.sh"]
