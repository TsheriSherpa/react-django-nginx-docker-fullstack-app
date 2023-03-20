FROM node:lts-alpine3.12 as build

WORKDIR /frontend

COPY frontend/package.json /frontend

COPY frontend/package-lock.json /frontend

RUN npm install

COPY frontend /frontend

EXPOSE 4000

ENTRYPOINT ["sh", "/frontend/entrypoint.sh"]
