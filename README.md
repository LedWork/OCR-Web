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
MAIL_SERVER=                    # SMTP server address (e.g., smtp.gmail.com)
MAIL_PORT=                      # SMTP server port (e.g., 587 for TLS)
MAIL_USERNAME=                  # Email address used for sending emails
MAIL_PASSWORD=                  # Password or app-specific password for the email account
WEB_SERVER_URL=                 # Full URL of the web server (e.g., https://ocr-pck.eu)
ADMIN_LOGIN=                    # Login for the admin account
ADMIN_PASSWORD=                 # Password for the admin account
MODEL_API_KEY=                  # API key for the OCR model
PASSWORD_VALIDITY_MINUTES=      # How long generated passwords remain valid (in minutes)
MONGO_USER=                     # MongoDB username
MONGO_PASSWORD=                 # MongoDB password
SECRET_KEY=                     # Secret key for Flask session encryption, CSRF protection, and secure cookie signing
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