import base64
import io
import sys
sys.path.insert(0, '..')
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app.card.views import card_bp
from app.admin.views import admin_bp
from werkzeug.datastructures import FileStorage

def mock_getenv_side_effect(key, default=None):
    return {
        "MONGO_HOST": "localhost",
        "MONGO_PORT": "27017",
        "MONGO_USER": "root",
        "MONGO_PASS": "pass",
    }.get(key, default)

class TestPhotoRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(card_bp)
        self.app.register_blueprint(admin_bp)
        self.client = self.app.test_client()

    @patch('app.core.db.MongoClient')
    @patch('os.getenv')
    def test_upload_image(self, mock_getenv, mock_mongo_client):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db['images'] = mock_collection
        mock_mongo_client.return_value = mock_db

        image_code = "image_code.jpg"
        mock_collection.find = []

        mock_file = FileStorage(
            stream=io.BytesIO(b"fake image data"),
            filename="test_new.png",
            content_type="image/png"
        )

        response = self.client.post(
            f"/upload-image/{image_code}",
            data={"file": mock_file},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Photo successfully uploaded and linked to the card", response.json["message"])

    @patch('app.core.db.MongoClient')
    @patch('os.getenv')
    def test_wrong_image_type(self, mock_getenv, mock_mongo_client):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db['images'] = mock_collection
        mock_mongo_client.return_value = mock_db

        image_code = "image_code.jpg"
        mock_collection.find = []

        mock_file = FileStorage(
            stream=io.BytesIO(b"fake image data"),
            filename="test_new.pdf",
        )

        response = self.client.post(
            f"/upload-image/{image_code}",
            data={"file": mock_file},
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 415)
        self.assertIn("Invalid file type or no file selected", response.json["error"])

    @patch('app.core.db.MongoClient')
    @patch('os.getenv')
    def test_no_image(self, mock_getenv, mock_mongo_client):
        mock_db = MagicMock()
        mock_collection = MagicMock()
        mock_db['images'] = mock_collection
        mock_mongo_client.return_value = mock_db

        image_code = "image_code.jpg"
        mock_collection.find = []

        response = self.client.post(
            f"/upload-image/{image_code}",
            content_type="multipart/form-data"
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("No file provided", response.json["error"])

if __name__ == "__main__":
    unittest.main()