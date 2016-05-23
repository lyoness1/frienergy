"""Models and database functions for Frienergy project."""

from flask_sqlalchemy import SQLAlchemy

import datetime

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of Frienergy website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name=%s %s>" % (self.user_id,
                                                 self.first_name,
                                                 self.last_name)


class Contact(db.Model):
    """A class for contacts of the user"""

    __tablename__ = "contacts"

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    contact_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(128), nullable=True)
    cell_phone = db.Column(db.String(12), nullable=True)
    street = db.Column(db.String(256), nullable=True)
    city = db.Column(db.String(64), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)
    total_frienergy = db.Column(db.Float, nullable=True)
    avg_t_btwn_ints = db.Column(db.Float, nullable=True)
    t_since_last_int = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Contact: %s %s>" % (self.first_name, self.last_name)


class Note(db.Model):
    """a method of adding notes to contacts for interactions"""

    __tablename__ = "notes"

    note_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    contact_id = db.Column(db.Integer,
                           db.ForeignKey('contacts.contact_id'),
                           nullable=False)
    interaction_id = db.Column(db.Integer,
                               db.ForeignKey('interactions.interaction_id'),
                               nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Note id=%s with=%s text=%s>" % (
            self.note_id, self.contact_id, self.text)


class Interaction(db.Model):
    """A class to log interactions with contacts"""

    __tablename__ = "interactions"

    interaction_id = db.Column(db.Integer,
                               primary_key=True,
                               autoincrement=True)
    contact_id = db.Column(db.Integer,
                           db.ForeignKey('contacts.contact_id'),
                           nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'),
                        nullable=False)
    date = db.Column(db.Date,
                     nullable=False)
    frienergy = db.Column(db.Integer,
                          nullable=False)
    t_delta_since_last_int = db.Column(db.Integer,
                                       nullable=True)

    # establishes relationships with user, contact, and note tables
    user = db.relationship("User",
                           backref=db.backref("interactions", order_by=interaction_id))
    contact = db.relationship("Contact",
                              backref=db.backref("interactions", order_by=interaction_id))
    note = db.relationship("Note",
                           backref=db.backref("interaction"), uselist=False)
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Interaction id=%s with=%s, %s date=%s>" % (
            self.interaction_id,
            self.contact_id, self.user_id,
            self.date)


##############################################################################
# Helper functions

def example_data():
    """Create some sample data for use with testing."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Contact.query.delete()
    Interaction.query.delete()
    Note.query.delete()

    # Add a fake user
    u1 = User(first_name="First",
              last_name="Last",
              email="email@domain.com",
              password="password")
    db.session.add(u1)
    db.session.commit()

    # Add some fake contacts
    c1 = Contact(user_id=u1.user_id,
                 first_name="First_1",
                 total_frienergy=24,
                 avg_t_btwn_ints=3,
                 t_since_last_int=5)

    c2 = Contact(user_id=u1.user_id,
                 first_name="First_2",
                 total_frienergy=15,
                 avg_t_btwn_ints=8,
                 t_since_last_int=5)

    db.session.add_all([c1, c2])
    db.session.commit()

    # Add some fake interactions
    i3 = Interaction(contact_id=c1.contact_id,
                     user_id=u1.user_id,
                     date=datetime.date(2016, 5, 17),
                     frienergy=10,
                     t_delta_since_last_int=3)

    i2 = Interaction(contact_id=c1.contact_id,
                     user_id=u1.user_id,
                     date=datetime.date(2016, 5, 14),
                     frienergy=10,
                     t_delta_since_last_int=3)

    i1 = Interaction(contact_id=c1.contact_id,
                     user_id=u1.user_id,
                     date=datetime.date(2016, 5, 11),
                     frienergy=4,
                     t_delta_since_last_int=0)

    db.session.add_all([i1, i2, i3])
    db.session.commit()

    # Add a fake Note
    n = Note(contact_id=c1.contact_id,
             interaction_id=i1.interaction_id,
             text="This is a test note")

    db.session.add(n)
    db.session.commit()


def connect_to_db(app, db_uri="postgresql:///frienergy"):
    """Connect the database to this Flask app."""

    # Configure to use the PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if this module is run interactively, it will be
    # in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
