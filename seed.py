"""Utility file to seed ratings database from MovieLens data in seed-data/"""

from sqlalchemy import func
from model import User
from model import Interaction
from model import Contact
from model import Note

from model import connect_to_db, db
from server import app
import datetime


def load_users():
    """Load users from users.csv into database."""
    
    print "Users"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    # Read users.csv file and insert data
    data = open("seed-data/users.csv")
    for row in data: 
        row = row.rstrip()
        user_id, first_name, last_name, email, password, zipcode = row.split(",")
        # create an instance of the user class with the data
        user = User(user_id=user_id,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=password,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)
        print user
    data.close()
    # Once we're done, we should commit our work
    db.session.commit()


def load_contacts():
    """Load contacts from contacts.csv into database."""
    
    # Delete all ros in table so there won't be dupes
    # Contact.query.delete()

    # read contacts.csv file and insert data 
    data = open("seed-data/contacts.csv", 'rU')
    for row in data:
        row = row.rstrip()
        user_id, contact_id, first_name, last_name, email, cell_phone, street, city, state, zipcode, power = row.split(",")
        # creates an instance of the Contact class for each contact 
        contact = Contact(user_id=user_id,
                          contact_id=contact_id,
                          first_name=first_name,
                          last_name=last_name,
                          email=email,
                          cell_phone=cell_phone,
                          street=street,
                          city=city,
                          state=state,
                          zipcode=zipcode,
                          power=power)
        # add each movie to the session db
        db.session.add(contact)
        print contact
    data.close()
    # commit changes to db
    db.session.commit()


def load_interactions():
    """Load interactions from interactions.csv into database."""
    
    # Clears table of existing rows
    Interaction.query.delete()

    # Read interactions.csv and insert data
    data = open("seed-data/interactions.csv", 'rU')
    for row in data:
        user_id, contact_id, interaction_id = row.split(",")[:3]
        date, frienergy = row.split(",")[3:5]
        
        # convert date into datetime date object
        date = datetime.datetime.strptime(date, "%d-%b-%Y")

        # Create an instance of Interaction using info from seed data file
        interaction = Interaction(user_id=user_id,
                                  contact_id=contact_id,
                                  interaction_id=interaction_id,
                                  date=date,
                                  frienergy=frienergy)
        # Add interaction instance to db
        db.session.add(interaction)
    data.close()
    # Commit work to db
    db.session.commit()


def load_notes():
    """Load notes from notes.csv into database."""
    
    # Clears table of existing rows
    Note.query.delete()

    # Read interactions.csv and insert data
    for row in open("seed-data/notes.csv", 'rU'):
        row = row.rstrip()
        print row
        contact_id, interaction_id, note_id, text = row.split(",")
        # Create an instance of Interaction using info from seed data file
        note = Note(contact_id=contact_id,
                    interaction_id=interaction_id,
                    note_id=note_id,
                    text=text)
        # Add note instance to db
        db.session.add(note)
    # Commit work to db
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_users()
    print "Finished load_users"
    load_contacts()
    print "Finished load_contacts"
    load_interactions()
    print "Finished load_interactions"
    load_notes()
    print "Finished load_notes"
    set_val_user_id()
    print "Done!"
