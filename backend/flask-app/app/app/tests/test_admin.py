import sys
sys.path.insert(0, '../..')
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask, json
from app.admin.views import admin_bp
from app.auth.views import auth_bp
from datetime import datetime

class TestAdminRoutes(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(admin_bp, url_prefix='/admin')
        self.app.register_blueprint(auth_bp, url_prefix='/auth')
        self.client = self.app.test_client()
        self.app.secret_key = 'test_secret_key'
        self.app.testing = True

    @patch('app.admin.model.get_db')
    @patch('app.admin.model.send_welcome_email')
    def test_add_user_with_welcome_email_success(self, mock_send_welcome_email, mock_get_db):
        # Mock database
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None  # User doesn't exist
        mock_collection.insert_one.return_value = MagicMock(inserted_id='test_id')
        
        mock_db = {
            'users': mock_collection
        }
        mock_get_db.return_value = mock_db
        
        # Mock welcome email sending
        mock_send_welcome_email.return_value = True
        
        # Mock admin session
        with patch('app.auth.decorators.is_admin', return_value=True):
            user_data = {
                "login": "test@example.com",
                "name": "Test User"
            }
            
            response = self.client.post(
                "/admin/add-user",
                data=json.dumps(user_data),
                content_type="application/json"
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertIn("Welcome email sent to test@example.com", response.json["message"])
            
            # Verify welcome email was called
            mock_send_welcome_email.assert_called_once_with("test@example.com")

    @patch('app.admin.model.get_db')
    @patch('app.admin.model.send_welcome_email')
    def test_add_user_with_welcome_email_failure(self, mock_send_welcome_email, mock_get_db):
        # Mock database
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = None  # User doesn't exist
        mock_collection.insert_one.return_value = MagicMock(inserted_id='test_id')
        
        mock_db = {
            'users': mock_collection
        }
        mock_get_db.return_value = mock_db
        
        # Mock welcome email sending failure
        mock_send_welcome_email.return_value = False
        
        # Mock admin session
        with patch('app.auth.decorators.is_admin', return_value=True):
            user_data = {
                "login": "test@example.com",
                "name": "Test User"
            }
            
            response = self.client.post(
                "/admin/add-user",
                data=json.dumps(user_data),
                content_type="application/json"
            )
            
            self.assertEqual(response.status_code, 200)
            self.assertIn("failed to send welcome email", response.json["message"])
            
            # Verify welcome email was called
            mock_send_welcome_email.assert_called_once_with("test@example.com")

    @patch('app.admin.model.get_db')
    def test_add_user_already_exists(self, mock_get_db):
        # Mock database - user already exists
        mock_collection = MagicMock()
        mock_collection.find_one.return_value = {
            "login": "test@example.com",
            "name": "Existing User"
        }
        
        mock_db = {
            'users': mock_collection
        }
        mock_get_db.return_value = mock_db
        
        # Mock admin session
        with patch('app.auth.decorators.is_admin', return_value=True):
            user_data = {
                "login": "test@example.com",
                "name": "Test User"
            }
            
            response = self.client.post(
                "/admin/add-user",
                data=json.dumps(user_data),
                content_type="application/json"
            )
            
            self.assertEqual(response.status_code, 400)
            self.assertIn("already exists", response.json["message"])

    @patch('app.admin.model.get_db')
    def test_add_user_no_data(self, mock_get_db):
        # Mock admin session
        with patch('app.auth.decorators.is_admin', return_value=True):
            response = self.client.post(
                "/admin/add-user",
                data="",
                content_type="application/json"
            )
            
            self.assertEqual(response.status_code, 400)
            self.assertIn("No JSON data provided", response.json["message"])

    @patch('app.admin.model.send_welcome_email')
    def test_send_welcome_email_success(self, mock_send_welcome_email):
        from app.admin.model import send_welcome_email
        
        # Mock Flask-Mail
        with patch('app.admin.model.mail') as mock_mail:
            mock_mail.app.config.get.side_effect = lambda key: {
                'MAIL_SERVER': 'smtp.example.com',
                'MAIL_USERNAME': 'test@example.com',
                'MAIL_PASSWORD': 'password'
            }.get(key)
            
            mock_mail.default_sender = 'test@example.com'
            mock_mail.send.return_value = None
            
            # Mock environment variable
            with patch.dict('os.environ', {'WEB_SERVER_URL': 'https://test.example.com'}):
                result = send_welcome_email('user@example.com')
                
                self.assertTrue(result)
                mock_mail.send.assert_called_once()

    @patch('app.admin.model.send_welcome_email')
    def test_send_welcome_email_missing_config(self, mock_send_welcome_email):
        from app.admin.model import send_welcome_email
        
        # Mock Flask-Mail with missing configuration
        with patch('app.admin.model.mail') as mock_mail:
            mock_mail.app.config.get.return_value = None
            
            result = send_welcome_email('user@example.com')
            
            self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
