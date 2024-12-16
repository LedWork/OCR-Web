from unittest.mock import patch, MagicMock
import sys
sys.path.insert(0, '..')
import unittest
from flask import Flask, json
from app.card.views import card_bp
from app.admin.views import admin_bp
from functools import wraps
from bson import ObjectId


class TestCardRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(card_bp, url_prefix='/card')
        self.app.register_blueprint(admin_bp, url_prefix='/admin')
        self.client = self.app.test_client()
        self.app.secret_key = 'test_secret_key'
        self.app.testing = True


    @patch("app.card.model.get_db")
    def test_upload_distinct_card(self, mock_get_db):

        card_1 = {
            "login": "Jhon",
            "password": "Doe"
        }
        card_2 = {
            "login": "Jhon2",
            "password": "Doe2"
        }
        card_3 = {
            "login": "Jhon3",
            "password": "Doe3"
        }
        card_list = [card_1, card_2, card_3]

        mock_collection = MagicMock()
        mock_collection.find_one.return_value = [None]
        mock_db = {
            "cards": mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/admin/upload-data",
            data=json.dumps(card_list),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("All items loaded successfully.", response.json["message"])


    @patch("app.card.model.get_db")
    def test_upload_not_distinct_card(self, mock_get_db):

        card_1 = {
            "_id": "2138",
            "name": "John",
            "surname": "Doe21",
        }
        card_2 = {
            "_id": "2137",
            "name": "John",
            "surname": "Doe21",
        }

        card_list = [card_1]

        mock_collection = MagicMock()
        mock_collection.find_one.return_value = card_2
        mock_db = {
            "cards": mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/admin/upload-data",
            data=json.dumps(card_list),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("Card with the same _id already exists: 2138", response.json["error"])


    @patch("app.card.model.get_db")
    def test_upload_card_data_invalid_json(self, mock_get_db):
        invalid_json = '{"name": "John", "surname": "Doe"'
        mock_collection = MagicMock()
        mock_db = {
            "cards": mock_collection
        }
        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/admin/upload-data",
            data=invalid_json,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("No JSON data provided", response.json["error"])


    @patch("app.card.model.get_db")
    def test_correct_card_success(self, mock_get_db):
        correct_card_data = {
            "_id": str(ObjectId()),
            "name": "John",
            "surname": "Doe",
            "correct": 1
        }

        mock_collection = MagicMock()
        mock_collection.find_one.return_value = correct_card_data
        mock_db = {
            "cards" : mock_collection
        }

        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/card/correct",
            data=json.dumps(correct_card_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Card marked as correct and updated.", response.json["message"])


    @patch("app.card.model.get_db")
    def test_correct_card_no_id(self, mock_get_db):
        correct_card_data = {
            "name": "John",
            "surname": "Doe",
            "correct": 1
        }

        mock_collection = MagicMock()
        mock_collection.find_one.return_value = correct_card_data
        mock_db = {
            "cards" : mock_collection
        }

        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/card/correct",
            data=json.dumps(correct_card_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("No card ID provided", response.json["error"])


    @patch("app.card.model.get_db")
    def test_correct_card_not_in_db(self, mock_get_db):
        correct_card_data = {
            "_id": "2137",
            "name": "John",
            "surname": "Doe",
            "correct": 1
        }

        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None
        mock_db = {
            "cards" : mock_collection
        }

        mock_get_db.return_value = mock_db

        response = self.client.post(
            "/card/correct",
            data=json.dumps(correct_card_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 404)
        self.assertIn("Card not found", response.json["error"])


    def test_random_card_no_cards(self):
        self.login_as_mock_user()
        response = self.client.get("/card/random")
        print(response)
        self.assertEqual(response.status_code, 400)
        self.assertIn("No cards available in the database.", response.json["error"])

    # @patch("app.core.db.MongoClient")
    # @patch("os.getenv")
    # def test_upload_correct_random_card(self, mock_getenv, mock_mongo_client):
    #     mock_getenv.side_effect = mock_getenv_side_effect

    #     mock_db = MagicMock()
    #     mock_collection = MagicMock()
    #     mock_db['cards'] = mock_collection
    #     mock_mongo_client.return_value = mock_db

    #     mock_collection.insert_one.return_value = MagicMock(inserted_id=ObjectId("507f1f77bcf86cd799439011"))

    #     card_data = {
    #         "_id": ObjectId("507f1f77bcf86cd799439011"),
    #         "name": "John",
    #         "surname": "Doe21",
    #         "correct": 0
    #     }
    #     mock_collection.find.return_value = [card_data]
    #     mock_collection.find_one.side_effect = lambda query: (
    #         card_data if query["_id"] == card_data["_id"] else None
    #     )
    #     mock_collection.update_one.return_value = MagicMock(modified_count=1)

    #     response = self.client.post(
    #         "/admin/upload-data",
    #         data=json.dumps({"name": "John", "surname": "Doe21"}),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Card successfully uploaded.", response.json["message"])

    #     response = self.client.post(
    #         "/card/correct",
    #         data=json.dumps({"_id": str(card_data["_id"]), "name": "John", "surname": "Doe21"}),
    #         content_type='application/json'
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("Card marked as correct and updated.", response.json["message"])