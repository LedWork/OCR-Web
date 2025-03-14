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

## 5. Testing  
Visit [http://localhost:5000](http://localhost:5000/) to test the app.  

1. You need to create an admin user. A temporary button is provided for this (**not secure** and will be removed later).  
2. Log in with:  
   - **Username:** `admin`  
   - **Password:** `admin`  
3. Access the **Admin Panel**, where you can add users and data.  
4. From here, you can test all application functionalities.  
