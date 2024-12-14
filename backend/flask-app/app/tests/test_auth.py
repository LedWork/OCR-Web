import sys
sys.path.insert(0, '..')
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app.admin.views import admin_bp    #for registering users
from app.auth.views import auth_bp  #for session
from app.card.views import card_bp      #to test decorators
from datetime import datetime, timedelta
import bcrypt

class TestAuthRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(card_bp, url_prefix='/card')
        self.app.register_blueprint(admin_bp, url_prefix='/admin')
        self.app.register_blueprint(auth_bp, url_prefix='/auth')
        self.client = self.app.test_client()
        self.app.secret_key = 'test_secret_key'
        self.app.testing = True

    @patch('app.auth.model.get_db')
    def test_login_with_exisitng_data(self, mock_get_db):
        user = {
            "login": "Jhon",
            "password": "Doe"
        }

        mock_collection = MagicMock()
        hashed_password = bcrypt.hashpw("Doe".encode('utf-8'), bcrypt.gensalt())

        mock_collection.find_one.return_value = {
                "login": "Jhon", 
                "password": hashed_password
        }
        mock_db = {
            'users' : mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/auth/login",
            data=json.dumps(user),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Sucessfully logged in", response.json["message"])

    @patch('app.auth.model.get_db')
    def test_login_with_wrong_password(self, mock_get_db):
        user = {
            "login": "Jhon",
            "password": "Doe"
        }

        mock_collection = MagicMock()
        hashed_password = bcrypt.hashpw("Doe123".encode('utf-8'), bcrypt.gensalt())

        mock_collection.find_one.return_value = {
                "login": "Jhon", 
                "password": hashed_password
        }
        mock_db = {
            'users': mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/auth/login",
            data=json.dumps(user),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn("Login or password incorrect.", response.json["message"])

    @patch('app.auth.model.get_db')
    def test_login_no_data(self, mock_get_db):
        user = {
            "login": "",
            "password": ""
        }

        mock_collection = MagicMock()
        hashed_password = bcrypt.hashpw("Doe".encode('utf-8'), bcrypt.gensalt())

        mock_collection.find_one.return_value = {
                "login": "Jhon", 
                "password": hashed_password
        }
        mock_db = {
            'users' : mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/auth/login",
            data=json.dumps(user),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 401)
        self.assertIn("Login or password incorrect.", response.json["message"])

    @patch('app.auth.model.get_db')
    def test_session_exists(self, mock_get_db):
        user = {
            "login": "Jhon",
            "password": "Doe"
        }

        mock_collection = MagicMock()
        hashed_password = bcrypt.hashpw("Doe".encode('utf-8'), bcrypt.gensalt())

        mock_collection.find_one.return_value = {
                "login": "Jhon", 
                "password": hashed_password
        }
        mock_db = {
            'users' : mock_collection
        }
        mock_get_db.return_value = mock_db

        self.client.post(
            "/auth/login",
            data=json.dumps(user),
            content_type="application/json"
        )

        response = self.client.get(
            "/auth/session",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("OK", response.json["message"])

    @patch('app.admin.views.get_db')
    def test_register_distinct(self, mock_get_db):
        user = {
            "login": "Jhon",
            "password": "Doe"
        }

        mock_collection = MagicMock()

        mock_collection.find_one.return_value = {}
        mock_db = {
            'users' : mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/admin/add-user",
            data=json.dumps(user),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("user added sucessfully!", response.json["message"])

    @patch('app.admin.views.get_db')
    def test_register_with_existing_login(self, mock_get_db):
        user = {
            "login": "Jhon",
            "password": "Doe"
        }

        mock_collection = MagicMock()

        mock_collection.find_one.return_value = {
            "login": "Jhon",
            "password": "Doe"
        }
        mock_db = {
            'users' : mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/admin/add-user",
            data=json.dumps(user),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("user with this login already exists", response.json["message"])

    @patch('app.card.model.get_db')
    @patch('app.auth.model.get_db')
    def test_access_to_restricted_function_logged(self, mock_get_db_auth, mock_get_db_card):
        user = {
            "login": "Jhon",
            "password": "Doe"
        }

        mock_collection_users = MagicMock()
        mock_collection_cards = MagicMock()
        hashed_password = bcrypt.hashpw("Doe".encode('utf-8'), bcrypt.gensalt())
        mock_collection_users.find_one.return_value = {
            "login": "Jhon",
            "password": hashed_password
        }
        #in logic of get_random_card function collection.find was changed to collection.find_one
        #so we are now mocking the find_one.return_value insted of find.return_value
        mock_collection_cards.find_one.return_value = {
                "_id": "card1", "correct": 1
            }

        mock_db = {
            'users': mock_collection_users,
            'cards': mock_collection_cards
        }
        mock_get_db_auth.return_value = mock_db
        mock_get_db_card.return_value = mock_db

        self.client.post(
            "/auth/login",
            data=json.dumps(user),
            content_type="application/json"
        )

        response = self.client.get(
            "/card/random"
        )

        self.assertEqual(response.status_code, 200)

    @patch('app.card.model.get_db')
    def test_access_to_restricted_function_not_logged(self, mock_get_db):
        mock_collection_cards = MagicMock()

        mock_collection_cards.find.return_value = [
            {"_id": "card1"},
            {"_id": "card2"}
        ]
        mock_db = {
            'cards' : mock_collection_cards
        }
        mock_get_db.return_value = mock_db

        response = self.client.get(
            "/card/random"
        )

        self.assertEqual(response.status_code, 401)