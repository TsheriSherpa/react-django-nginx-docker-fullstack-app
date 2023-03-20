FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual .build-deps python3-dev musl-dev gcc  build-base \
    && apk add --no-cache mariadb-dev

RUN pip install --upgrade pip

RUN adduser -D docker

WORKDIR /app

# copy entrypoint.sh
COPY backend/entrypoint.sh /app
RUN sed -i 's/\r$//g' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

USER docker

COPY backend/requirements.txt /app

RUN pip install --user -r requirements.txt

COPY backend /app

EXPOSE 8000

ENTRYPOINT ["sh", "/app/entrypoint.sh"]