import json
from unittest import TestCase
from model import connect_to_db, db, User, Interaction, Contact, Note, example_data
import server
import helper
import datetime

class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.secret_key = "ABC"

        # Connect to test database
        connect_to_db(server.app, "postgresql:///testdb")

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
        """Tests the delete contact route"""

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

        # tests the case of a note attached to the interaction
        result = self.client.post('/getInteraction.json', data={'id': 1})
        self.assertIn("This is a test note", result.data)

        # tests the case of a note not attached to the itneraction
        result = self.client.post('/getInteraction.json', data={'id': 2})
        self.assertNotIn("This is a test note", result.data)


    def test_edit_interaction(self):
        """Tests the edit_interaction route"""

        # tests the case of a note pre-existing and being updated
        result = self.client.post('/editInteraction',
                    data= {
                        'interaction-id': 3,
                        'date': datetime.date(2016, 5, 11),
                        'frienergy': 9,
                        'notes': "Updated note",
                        'note-id': 1,
                    }, follow_redirects=True)
        self.assertIn("First's Profile", result.data)

        # tests the case of a new note being added to the interaction
        result = self.client.post('/editInteraction',
                    data= {
                        'interaction-id': 2,
                        'date': datetime.date(2016, 5, 14),
                        'frienergy': 9,
                        'notes': "New note",
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
        self.assertIn("First_1", result.data)

################################################################################
# Tests for HELPER FUNCTIONS

    def test_sort_interactions_by_date(self):
        """Tests the sort interactions by date helper function"""

        result = helper.sort_user_interactions_by_date(1)
        self.assertEqual(len(result), 3)


    def test_get_and_sort_contacts_by_power(self):
        """Tests the get_and_sort_contacts_by_power helper function"""

        result = helper.get_and_sort_contacts_by_power(1)
        self.assertEqual(len(result), 2)


    def test_calculate_t_delta_since_last_int(self):
        """Tests the calculate_t_delta_since_last_int helper function"""

        helper.calculate_t_delta_since_last_int(1)
        int_list = db.session.query(Interaction).filter(Interaction.contact_id == 1).all()
        self.assertEqual(int_list[2].t_delta_since_last_int, 3)


    def test_update_t_since_last_int(self):
        """Tests the update_t_since_last_int helper function"""

        result = helper.update_t_since_last_int(1)
        self.assertNotEqual(Contact.query.get(1).t_since_last_int, -1)


    def test_update_total_frienergy(self):
        """Tests the update_total_frienergy helper function"""

        result = helper.update_total_frienergy(1)
        self.assertEqual(Contact.query.get(1).total_frienergy, 24)


    def test_update_avg_t_btwn_ints(self):
        """Tests the update_avg_t_btwn_ints helper function"""

        # tests the case where the contact has multiple interactions
        helper.update_avg_t_btwn_ints(1)
        self.assertEqual(Contact.query.get(1).avg_t_btwn_ints, 3)

        # tests the case where the contact has no interactions
        helper.update_avg_t_btwn_ints(2)
        self.assertEqual(Contact.query.get(2).avg_t_btwn_ints, 0)


    def test_calculate_power(self):
        """Tests the calculate_power helper function"""

        self.assertEqual(helper.calculate_power(1), 8.0)


if __name__ == "__main__":
    import unittest

    unittest.main()
