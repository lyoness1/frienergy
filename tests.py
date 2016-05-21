import json
from unittest import TestCase
from model import connect_to_db, db, User, Interaction, Contact, Note, example_data
from server import app
import server

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.secret_key = "ABC"

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Streamline your social interactions", result.data)


    def test_show_dashboard(self):
        """Test dashboard page."""

        result = self.client.get("/dashboard/1")
        self.assertIn("First's Profile", result.data)


    def test_login(self):
        """Test login modal."""

        # a test for the case of correct email/password
        result = self.client.post("/login", 
                                  data={"email": "email@domain.com",
                                        "password": "password"},
                                  follow_redirects=True)
        self.assertIn("First's Profile", result.data)

        # a test for the case of correct email, wrong password
        result = self.client.post("/login", 
                                  data={"email": "email@domain.com",
                                        "password": "wrong"},
                                  follow_redirects=True)
        self.assertIn("Incorrect credentials", result.data)

        # a test for the case of no user registered
        result = self.client.post("/login", 
                                  data={"email": "wrong_email@domain.com",
                                        "password": "password"},
                                  follow_redirects=True)
        self.assertIn("No user registered with that email", result.data)


    def test_register(self):
        """Tests the registration route"""

        result = self.client.post("/register", data={
                'first-name': 'Joe',
                'last-name': 'Schmoe',
                'email': 'email@place.com',
                'zipcode': '12345',
                'password': 'notsafe'
            }, follow_redirects=True)
        self.assertIn("Joe's Profile", result.data)

if __name__ == "__main__":
    import unittest

    unittest.main()
