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
    @patch('os.getenv', side_effect=mock_getenv_side_effect)
    def test_upload_new_photo(self, mock_getenv, mock_mongo_client):
        mock_collection = MagicMock()
        mock_mongo_client.return_value = {"images": mock_collection}

        image_code = "new_image_code.jpg"
        mock_collection.find = []

        print(mock_collection.find)

        mock_file = FileStorage(
            stream=io.BytesIO(b"fake updated image data"),
            filename="test_updated.png",
            content_type="image/png"
        )

        response = self.client.post(
            f"/upload-image/{image_code}",
            data={"file": mock_file},
            headers={"Action": "new"},
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Photo successfully uploaded", response.json["message"])

    @patch('app.core.db.MongoClient')
    @patch('os.getenv', side_effect=mock_getenv_side_effect)
    def test_update_existing_photo(self, mock_getenv, mock_mongo_client):
        mock_collection = MagicMock()
        mock_mongo_client.return_value = {"images": mock_collection}

        image_code = "existing_image_code.jpg"
        mock_collection.find.return_value = [{"_id": image_code, "photo": "existing_data"}]

        print(mock_collection.find.return_value)

        mock_file = FileStorage(
            stream=io.BytesIO(b"fake updated image data"),
            filename="test_updated.png",
            content_type="image/png"
        )

        response = self.client.post(
            f"/upload-image/{image_code}",
            data={"file": mock_file},
            headers={"Action": "update"},
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Photo successfully updated", response.json["message"])

    @patch('app.core.db.MongoClient')
    @patch('os.getenv', side_effect=mock_getenv_side_effect)
    def test_invalid_action(self, mock_getenv, mock_mongo_client):
        mock_collection = MagicMock()
        mock_mongo_client.return_value = {"images": mock_collection}

        image_code = "invalid_action_image_code.jpg"
        mock_file = (io.BytesIO(b"fake image data"), "test.png")

        response = self.client.post(
            f"/upload-image/{image_code}",
            data={"file": mock_file},
            headers={"Action": "invalid_action"},
            content_type="multipart/form-data"
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid action", response.json["error"])

if __name__ == "__main__":
    unittest.main()