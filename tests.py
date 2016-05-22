import json
from unittest import TestCase
from model import connect_to_db, db, User, Interaction, Contact, Note, example_data
from server import app
import server
import datetime

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

        # inputs sample data for testing from model.py
        example_data()

        # establish a client session for use in tests
        with self.client as c:
            with c.session_transaction() as sess:
                sess['logged_in_user_id'] = 1
                sess['logged_in_email'] = 'email@domain.com'
                sess['logged_in_user_name'] = 'First'

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

################################################################################
# Tests for routes to handle RENDERING PAGES

    def test_index(self):
        """Test homepage page."""

        result = self.client.get("/")
        self.assertIn("Streamline your social interactions", result.data)


    def test_show_dashboard(self):
        """Test dashboard page."""

        result = self.client.get("/dashboard/1")
        self.assertIn("First's Profile", result.data)

################################################################################
# Tests for routes to handle LOGIN and LOGOUT

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


    def test_logout(self):
        """Tests the logout route"""

        result = self.client.get('/logout', follow_redirects=True)
        self.assertIn("Streamline your social interactions", result.data)


    def test_get_user(self):
        """Test the get_user() route"""

        result = self.client.get('/getUser.json')
        self.assertIn("email@domain.com", result.data)


    def test_edit_profile(self):
        """Tests the edit_profile route"""

        result = self.client.post('/editProfile', data={
                    'first-name': 'First',
                    'last-name': 'Last',
                    'email': 'email@place.com',
                    'zipcode': '12345',
                    'password': 'notsafe'
                }, follow_redirects=True)

        self.assertIn("First's Profile", result.data)

################################################################################
# Tests for routes to handle adding/deleting/editing CONTACTS 

    def test_add_contact(self):
        """Tests the add contact route"""

        result = self.client.post('/addContact', data={'first-name': 'First_3'},
                                  follow_redirects=True)
        self.assertIn("First's Profile", result.data)


    def test_get_contact(self):
        """Tests the get_contact route"""

        result = self.client.post('/getContact.json', data={'id': 1},
                                   follow_redirects=True)
        self.assertIn("This is a test note", result.data)


    def test_edit_contact(self):
        """Tests the add contact route"""

        result = self.client.post('/editContact', data={
                        'contact-id': 1,
                        'first-name': 'First_1'},
                        follow_redirects=True)
        self.assertIn("First's Profile", result.data)


    def test_delete_contact(self):
        """Tests the add contact route"""

        result = self.client.post('/deleteContact', data={
                        'contact-id': 1}, follow_redirects=True)
        self.assertIn("First's Profile", result.data)

################################################################################
# Tests for routes to handle adding/deleting/editing and INTERACTIONS

    def test_add_interaction(self):
        """Tests the add_interaction route"""

        result = self.client.post('/addInteraction',
                    data={
                        'contact-id': 1,
                        'frienergy': 3,
                        'date': datetime.date(2016, 4, 5),
                        'notes': "This is a note",
            }, follow_redirects=True)
        self.assertIn("First's Profile", result.data)


    def test_get_interaction(self):
        """Tests the get_interaction route"""

        result = self.client.post('/getInteraction.json', data={'id': 1})
        self.assertIn("This is a test note", result.data)


    def test_edit_interaction(self):
        """Tests the edit_interaction route"""

        result = self.client.post('/editInteraction',
                    data= {
                        'interaction-id': 1,
                        'date': datetime.date(2016, 5, 14),
                        'frienergy': 9,
                        'notes': "Updated note",
                        'note-id': 1,
                    }, follow_redirects=True)
        self.assertIn("First's Profile", result.data)


    def test_delete_interaction(self):
        """Tests the delete_interaction route"""

        result = self.client.post('/deleteInteraction',
                    data={'interaction-id': 1}, follow_redirects=True)
        self.assertIn("First's Profile", result.data)


################################################################################
# Routes to handle NOTES

    def test_get_note(self):
        """Tests the get_note route"""

        result = self.client.get('/getNote.json?id=1')
        self.assertEqual(result.status_code, 200)


################################################################################
# Tests for routes to get and post REMINDERS

    def test_calculate_reminders(self):
        """Tests the calculate_reminders route"""

        result = self.client.post('/getReminders.json')
        self.assertEqual(result.status_code, 200)

if __name__ == "__main__":
    import unittest

    unittest.main()
