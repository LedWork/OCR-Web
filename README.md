# How to Run the Application?

## 1. Install Required Programs  
Install **npm** to build the frontend. Follow [this tutorial](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm).  

Then, in the `frontend/app` directory, run:  
```sh
npm install
```
This will install all required dependencies.  

## 2. Building the Frontend  
Navigate to `frontend/app` and run:  
```sh
./build.sh
```
This will create a `dist` folder inside `backend/flask-app/app`, which is required for the backend.  

## 3. Preparing the Backend  
Create a `.env` file in `backend/flask-app/app/app/` with the following template:  
```ini
MAIL_SERVER=
MAIL_PORT=
MAIL_USERNAME=
MAIL_PASSWORD=
```
By default, the configuration uses **TLS**, but this can be changed in `__init__.py` within the same directory as the `.env` file.  

## 4. Building and Running the Application  
Install **Docker** and **Docker Compose**.  

Then, navigate to `backend/flask-app` and run:  
```sh
docker-compose up --build
```
This will build and start the Docker container.  


## Deployment with certbot certificates - only first time

Note: http and https traffic must be enabled in cloud console

```
docker compose -f docker-compose-deploy.yaml down --volumes
sudo rm -rf /etc/letsencrypt/
mkdir -p nginx/certbot/{www,conf}
cp nginx/nginx-http-only.conf nginx/nginx.conf
docker compose -f docker-compose-deploy.yaml up --build -d
sudo certbot certonly --webroot -w ~/OCR-Web/nginx/certbot/www -d ocr-pck.eu -d www.ocr-pck.eu --non-interactive --agree-tos -m
skany.hdkpck@pck.pomorze.pl -v
docker stop nginx_proxy
cp nginx/nginx-full-ssl.conf nginx/nginx.conf
docker compose -f docker-compose-deploy.yaml up --build -d
```