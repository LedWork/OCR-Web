import unittest
import sys
sys.path.insert(0, '../..')
from unittest.mock import patch, MagicMock
from app.core.db import get_db



class TestDBConfig(unittest.TestCase):

    def mock_getenv_side_effect(self, key, default=None):
        return {
            "MONGO_HOST": "localhost",
            "MONGO_PORT": "27017",
            "MONGO_USER": "root",
            "MONGO_PASS": "pass",
        }.get(key, default)

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_get_db_with_default_values(self, mock_getenv, mock_mongo_client):
        mock_getenv.side_effect = self.mock_getenv_side_effect
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        db = get_db()
        mock_mongo_client.assert_called_with(
            host="localhost",
            port=27017,
            username="root",
            password="pass",
        )
        self.assertEqual(db, mock_client["animal_db"])

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_get_db_with_custom_values(self, mock_getenv, mock_mongo_client):
        mock_getenv.side_effect = lambda key, default=None: {
            "MONGO_HOST": "mongo_host",
            "MONGO_PORT": "28017",
            "MONGO_USER": "custom_user",
            "MONGO_PASS": "custom_pass",
        }.get(key, default)
        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        db = get_db()
        mock_mongo_client.assert_called_with(
            host="mongo_host",
            port=28017,
            username="custom_user",
            password="custom_pass",
        )
        self.assertEqual(db, mock_client["animal_db"])

    @patch("app.core.db.MongoClient")
    def test_get_db_no_connection(self, mock_mongo_client):
        mock_mongo_client.side_effect = Exception("Database connection failed")
        with self.assertRaises(Exception):
            get_db()

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_insert_data(self, mock_getenv, mock_mongo_client):
        mock_getenv.side_effect = self.mock_getenv_side_effect

        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        db = get_db()

        collection = mock_client["animal_db"]["animals"]
        collection.insert_one.return_value = {"inserted_id": "123456"}

        inserted_data = collection.insert_one({"name": "Lion", "type": "Wild"})

        collection.insert_one.assert_called_with({"name": "Lion", "type": "Wild"})
        self.assertEqual(inserted_data, {"inserted_id": "123456"})

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_retrieve_data(self, mock_getenv, mock_mongo_client):
        mock_getenv.side_effect = self.mock_getenv_side_effect

        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        db = get_db()

        collection = mock_client["animal_db"]["animals"]
        collection.find_one.return_value = {"name": "Lion", "type": "Wild"}

        retrieved_data = collection.find_one({"name": "Lion"})

        collection.find_one.assert_called_with({"name": "Lion"})
        self.assertEqual(retrieved_data, {"name": "Lion", "type": "Wild"})

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_retrieve_data_not_found(self, mock_getenv, mock_mongo_client):
        mock_getenv.side_effect = self.mock_getenv_side_effect

        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        db = get_db()

        collection = mock_client["animal_db"]["animals"]
        collection.find_one.return_value = None

        retrieved_data = collection.find_one({"name": "Tiger"})

        collection.find_one.assert_called_with({"name": "Tiger"})
        self.assertIsNone(retrieved_data)

    @patch("app.core.db.MongoClient")
    @patch("os.getenv")
    def test_insert_data_error(self, mock_getenv, mock_mongo_client):
        mock_getenv.side_effect = self.mock_getenv_side_effect

        mock_client = MagicMock()
        mock_mongo_client.return_value = mock_client
        db = get_db()

        collection = mock_client["animal_db"]["animals"]
        collection.insert_one.side_effect = Exception("Insert failed")

        with self.assertRaises(Exception):
            collection.insert_one({"name": "Elephant", "type": "Wild"})


if __name__ == "__main__":
    unittest.main()
