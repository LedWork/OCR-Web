FROM node:lts-alpine

WORKDIR /app

RUN npm install -g http-server && \
    npm install && \
    npm run build

COPY . .

EXPOSE 8080

CMD ["http-server", "dist"]
