import unittest
from app.extension import db
from app.models import User
from app.auth import login, logout, current_user
from app import create_app

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user
        self.user = User(username="testuser", email="testuser@example.com", password="testpassword")
        db.session.add(self.user)
        db.session.commit()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login(self):
        response = self.client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Login successful")

    def test_logout(self):
        response = self.client.post("/auth/logout")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["message"], "Logout successful")

    def test_current_user(self):
        # Login first
        login_response = self.client.post("/auth/login", json={"username": "testuser", "password": "testpassword"})
        self.assertEqual(login_response.status_code, 200)

        response = self.client.get("/auth/current_user")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["user"]["username"], "testuser")
        self.assertEqual(data["user"]["email"], "testuser@example.com")

if __name__ == "__main__":
    unittest.main()
