import unittest
import json
from flask import Flask
from app.extension import db
from app.models.user import User
from app.auth.user_auth import auth_bp

class UserAuthTestCase(unittest.TestCase):
    def setUp(self):
        # Create a test Flask app
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.register_blueprint(auth_bp)

        # Initialize a test client
        self.client = self.app.test_client()

        # Create an in-memory SQLite database for testing
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_login(self):
        # Add a test user to the database
        with self.app.app_context():
            user = User(username='testuser', password='testpassword')
            db.session.add(user)
            db.session.commit()

        # Test the login route
        response = self.client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
        data = json.loads(response.data.decode())

        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)

    def test_logout(self):
        # Test the logout route
        response = self.client.get('/logout')

        self.assertEqual(response.status_code, 200)
        self.assertIn('Logged out successfully', response.data.decode())

    # def test_current_user(self):
    #     # Test the current_user route
    #     response = self.client.get('/current_user', headers={'Authorization': 'Bearer your_access_token_here'})
    #     data = json.loads(response.data.decode())

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('logged_in_as', data)

    # def test_protected_resource(self):
    #     # Test the protected_resource route
    #     response = self.client.get('/protected/resource', headers={'Authorization': 'Bearer your_access_token_here'})
    #     data = json.loads(response.data.decode())

    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('message', data)
    #     self.assertEqual(data['message'], 'This is a protected resource.')

if __name__ == '__main__':
    unittest.main()
