# OCR-Web

## How to test?
### 1.
Go to the ```frontend/app``` and run ```./build.sh```. This will create a ```dist``` folder in ```backend/flask-app``` which is required.
### 2. 
Go to the ```backend/flask-app``` and run ```docker-compose up --build``` to create the docker container.
### 3. 
Visit [http://localhost:5000](http://localhost:5000/) to test the app. You need to create an admin user. We added a temporary button which will do this for you (it's not secure and will be deleted). Then, you can log in with username: ```admin``` and password: ```admin```. Next, you can go to admin panel, where you can:
<br>a) upload a JSON file with the data (```test.json``` can be found on discord).
<br>b) upload an image (this is optional) related to the uploaded data (the image name is important).
<br>c) add a new user by typing login, and a password will be generated for this login.
