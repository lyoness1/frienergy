"""Models and database functions for Frienergy project."""

from flask_sqlalchemy import SQLAlchemy

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
    user = db.relationship("User",
                           backref=db.backref("interactions", order_by=interaction_id))
    contact = db.relationship("Contact",
                              backref=db.backref("interactions", order_by=interaction_id))
    note = db.relationship("Note",
                           backref=db.backref("interactions", order_by=interaction_id))
    t_delta_since_last_int = db.Column(db.Integer,
                                       nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Interaction id=%s with=%s, %s date=%s>" % (
            self.interaction_id,
            self.contact_id, self.user_id,
            self.date)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to this Flask app."""

    # Configure to use the PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///frienergy'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if this module is run interactively, it will be
    # in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
