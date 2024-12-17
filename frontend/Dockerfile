FROM node:lts-alpine

WORKDIR /app

COPY app/package.json app/package-lock.json ./

RUN npm install -g http-server && npm install

COPY ./app ./

RUN npm run build

EXPOSE 8080
CMD ["http-server", "dist"]

