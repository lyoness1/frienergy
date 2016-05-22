"""Frienergy, by Allison Lyon, 2016"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Contact, Interaction, Note
from helper import *

import datetime
import json


app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


################################################################################
# Routes to handle RENDERING PAGES
@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route('/dashboard/<int:user_id>')
def show_dashboard(user_id):
    """Shows the dashboard for the current user"""

    # returns the user object to be able to display their profile information
    user = User.query.get(user_id)

    # returns a list of tupes for all interactions of user: (interaction, date)
    # list is sorted with newest interaction first
    interactions = sort_user_interactions_by_date(user_id)

    # returns a list of lists: [power-%, fname, lname, contact_id]
    # list is sorted by highest power percentage first
    contacts = get_and_sort_contacts_by_power(user_id)

    # renders the dashboard.html page with user's contact and interaction data
    return render_template("dashboard.html",
                           user=user,
                           interactions=interactions,
                           contacts=contacts)


################################################################################
# Routes to handle LOGIN and LOGOUT

@app.route('/login', methods=["POST"])
def login():
    """Handles user login"""

    # gets email and password from the form
    email = request.form.get('email')
    password = request.form.get('password')

    # gets a user object from the database by email
    db_user = db.session.query(User).filter(User.email == email).first()

    # handles login of existing user
    if db_user:
        if password == db_user.password:
            # flash message
            # return render_template("homepage.html")
            # add username to session
            flash("Successfully logged in.")
            session['logged_in_email'] = db_user.email
            session['logged_in_user_id'] = db_user.user_id
            session['logged_in_user_name'] = db_user.first_name
            return redirect("/dashboard/"+str(db_user.user_id))
        else:
            flash("Incorrect credentials. Please try again or register.")
            # flash message alerting them to incorrect password
            # redirect back to homepage
            return redirect("/")
    else:
        # redirect to the registration
        flash("No user registered with that email. " +
              "Please check your login information or create an account.")
        return redirect('/')


@app.route('/register', methods=['POST'])
def register():
    """creates a user profile for a new user"""

    # gets user infor from the registration form
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('email')
    zipcode = request.form.get('zipcode')
    password = request.form.get('password')

    # creates an instance for the user in the db with the gathered information
    new_user = User(first_name=first_name,
                    last_name=last_name,
                    email=email,
                    zipcode=zipcode,
                    password=password)
    db.session.add(new_user)
    db.session.commit()

    # adds user information to the session for use later
    session['logged_in_email'] = email
    session['logged_in_user_id'] = new_user.user_id
    session['logged_in_user_name'] = new_user.first_name

    flash("You have successfully registred! You are now logged in.")
    return redirect("/dashboard/"+str(new_user.user_id))


@app.route('/logout')
def logout():
    """logs user out"""

    # removes user from session
    session.pop("logged_in_email", None)
    session.pop("logged_in_user_id", None)
    session.pop("logged_in_user_name", None)

    # gives user feedback on their logout action
    flash("You have been logged out.")

    # routes to homepage
    return redirect("/")


@app.route('/getUser.json', methods=['GET'])
def get_user():
    """gets the logged in user's information to prepopulate edit profile form"""

    # gets current user from session
    user_id = session['logged_in_user_id']
    user = User.query.get(user_id)

    # creates a dictionary to send to prepopulate edit profile modal form
    user_info = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'zipcode': user.zipcode,
    }

    return jsonify(user_info)


@app.route('/editProfile', methods=['POST'])
def edit_profile():
    """updates the profile information of the logged in user"""

    # gets current user from session
    user_id = session['logged_in_user_id']
    user = User.query.get(user_id)

    user.first_name = request.form.get('first-name')
    user.last_name = request.form.get('last-name')
    user.email = request.form.get('email')
    user.zipcode = request.form.get('zipcode')
    user.password = request.form.get('password')

    # gives user feedback on their logout action
    flash("You have successfully updated your profile information.")

    # routes to homepage
    return redirect("/dashboard/"+str(user_id))



################################################################################
# Routes to handle adding/deleting/editing CONTACTS 

@app.route('/addContact', methods=['POST'])
def add_contact():
    """Adds a contact to the db"""

    # gets current user's id
    user_id = session['logged_in_user_id']

    # gets contact information from form
    first_name = request.form.get('first-name')
    last_name = request.form.get('last-name')
    email = request.form.get('contact-email')
    cell_phone = request.form.get('cell-phone')
    street = request.form.get('street')
    city = request.form.get('city')
    state = request.form.get('state')
    zipcode = request.form.get('zipcode')

    # creates an instance for the contact and adds them to the db
    new_contact = Contact(user_id=user_id,
                          first_name=first_name,
                          last_name=last_name,
                          email=email,
                          cell_phone=cell_phone,
                          street=street,
                          city=city,
                          state=state,
                          zipcode=zipcode,
                          total_frienergy=0,
                          avg_t_btwn_ints=0,
                          t_since_last_int=0)

    db.session.add(new_contact)
    db.session.commit()

    flash("Contact successfully added.")
    return redirect("/dashboard/"+str(user_id))


@app.route('/getContact.json', methods=['POST'])
def get_contact():
    """gets contact information from db for edit contact form"""

    # retrieves existing contact object from db
    contact_id = request.form.get('id')
    c = Contact.query.get(contact_id)

    # calculates interesting metrics for a relationship's health 
    all_interactions = db.session.query(Interaction).filter(Interaction
                                        .contact_id == contact_id).all()
    total_interactions = len(all_interactions)
    avg_power = calculate_power(contact_id)
    avg_frienergy_per_int = round(sum(i.frienergy for i in all_interactions) / total_interactions, 1)
    
    # gets all notes for a particular contact 
    notes = {}
    for i in all_interactions:
        if i.note:
            date = i.date.strftime('%Y-%m-%d')
            notes[date] = i.note.text
 
    # creates a dictionary of contact info to pass through JSON to HTML script
    contact_info = {
        'contact_id': c.contact_id,
        'first_name': c.first_name,
        'last_name': c.last_name,
        'email': c.email,
        'cell_phone': c.cell_phone,
        'street': c.street,
        'city': c.city,
        'state': c.state,
        'zipcode': c.zipcode,
        'total_frienergy': c.total_frienergy,
        'avg_t_btwn_ints': c.avg_t_btwn_ints,
        't_delta_since_last_int': c.t_since_last_int,
        'total_interactions': total_interactions,
        'avg_power': avg_power,
        'avg_frienergy_each_interaction': avg_frienergy_per_int,
        'notes': notes,
    }

    return jsonify(contact_info)


@app.route('/editContact', methods=['POST'])
def edit_contact():
    """updates a contact's information"""

    # gets contact from edit-contact form
    contact_id = int(request.form.get('contact-id'))
    c = Contact.query.get(contact_id)

    # gets contact information from form
    c.first_name = request.form.get('first-name')
    c.last_name = request.form.get('last-name')
    c.email = request.form.get('contact-email')
    c.cell_phone = request.form.get('cell-phone')
    c.street = request.form.get('street')
    c.city = request.form.get('city')
    c.state = request.form.get('state')
    c.zipcode = request.form.get('zipcode')

    db.session.commit()

    flash("Contact successfully updated.")

    # redirects to user's dashboard
    user_id = session['logged_in_user_id']
    return redirect("/dashboard/"+str(user_id))


@app.route('/deleteContact', methods=['POST'])
def delete_contact():
    """deletes a contact from the db"""

    # gets contact from edit-contact form
    contact_id = int(request.form.get('contact-id'))

    # deletes all notes corresponding to contact
    notes = db.session.query(Note).filter(Note.contact_id == contact_id).all()
    for n in notes:
        db.session.delete(n)

    # deletes all interactions corresponding to contact
    interactions = db.session.query(Interaction).filter(Interaction.contact_id == contact_id).all()
    for i in interactions:
        db.session.delete(i)

    # deletes contact object from db
    db.session.delete(Contact.query.get(contact_id))
    db.session.commit()

    flash("Contact successfully deleted.")

    # redirects to user's dashboard
    user_id = session['logged_in_user_id']
    return redirect("/dashboard/"+str(user_id))

################################################################################
# Routes to handle adding/deleting/editing and INTERACTIONS

@app.route('/addInteraction', methods=['POST'])
def add_interaction():
    """Adds an interaction to the db"""

    # gets current user's id from session
    user_id = session['logged_in_user_id']

    # gets info from add-interaction form
    contact_id = int(request.form.get('contact-id'))
    frienergy = int(request.form.get('frienergy'))

    # gets data from add interaction form and converts to date object
    date = request.form.get('date')
    date = datetime.datetime.strptime(date, '%Y-%m-%d').date()

    # creates an interaction instance for the contact and adds it to the db
    new_interaction = Interaction(user_id=user_id,
                                  contact_id=contact_id,
                                  date=date,
                                  frienergy=frienergy)
    db.session.add(new_interaction)
    db.session.flush()

    # gets note as string and converts to note object
    text = request.form.get('notes')
    if text:
        new_note = Note(contact_id=contact_id,
                        interaction_id=new_interaction.interaction_id,
                        text=text)
        db.session.add(new_note)

    db.session.commit()

    # calculates the *Interaction* attributes (plural): time since last interaction
    # can only be called after instantiating new interaction; order CAN be wrong
    calculate_t_delta_since_last_int(contact_id)

    # update all necessary contact attributes with new interaction data
    update_avg_t_btwn_ints(contact_id)
    update_total_frienergy(contact_id)
    update_t_since_last_int(contact_id)

    # provides user feedback that interaction has been added
    flash("Interaction successfully added.")

    return redirect("/dashboard/"+str(user_id))


@app.route('/getInteraction.json', methods=['POST'])
def get_interaction():
    """gets interaction information from db for edit interaction form"""

    # retrieves existing contact object from db
    interaction_id = int(request.form.get('id'))
    i = Interaction.query.get(interaction_id)

    # formates datetime date object to be readable by json
    date_string = i.date.strftime('%Y-%m-%d')

    # gets contact name for form
    c = Contact.query.get(i.contact_id)
    contact_name = str(c.first_name) + " " + str(c.last_name)

    # pulls text of note, if note was created
    if i.note:
        note_text = i.note.text
        note_id = i.note.note_id
    else:
        note_text = ""
        note_id = None

    # creates a dictionary of contact info to pass through JSON to HTML script
    interaction_info = {
        'interactionId': interaction_id,
        'contactName': contact_name,
        'date': date_string,
        'frienergy': i.frienergy,
        'noteId': note_id,
        'noteText': note_text,
    }

    return jsonify(interaction_info)

@app.route('/editInteraction', methods=['POST'])
def edit_interaction():
    """updates an interaction"""

    # gets interaction object from edit-interaction form
    interaction_id = int(request.form.get('interaction-id'))
    i = Interaction.query.get(interaction_id)

    # gets and formats interaction date
    date = request.form.get('date')

    # updates interaction attributes and commits changes to db
    i.frienergy = request.form.get('frienergy')
    i.date = date

    # gets note as string
    # if previous note, updates text attr, otherwise, creates new note
    text = request.form.get('notes')
    note_id = request.form.get('note-id')
    if note_id:
        note = Note.query.get(note_id)
        note.text = text
    elif text != "":
        note = Note(contact_id=i.contact_id,
                    interaction_id=interaction_id,
                    text=text)
        db.session.add(note)

    db.session.commit()

    flash("Interaction successfully updated.")

    # redirects to user's dashboard
    user_id = session['logged_in_user_id']
    return redirect("/dashboard/"+str(user_id))


@app.route('/deleteInteraction', methods=['POST'])
def delete_interaction():
    """deletes an interaction from the db"""

    # gets interaction object from edit-interaction form
    interaction_id = int(request.form.get('interaction-id'))
    i = Interaction.query.get(interaction_id)

    # deletes note corresponding to interaction
    if i.note:
        db.session.delete(Note.query.get(interaction_id))

    # deletes interaction object from db
    db.session.delete(Interaction.query.get(interaction_id))
    db.session.commit()

    flash("Interaction successfully deleted.")

    # redirects to user's dashboard
    user_id = session['logged_in_user_id']
    return redirect("/dashboard/"+str(user_id))

################################################################################
# Routes to handle NOTES

@app.route('/getNote.json', methods=['GET'])
def get_note():
    """retreives note text from db"""

    interaction_id = request.args.get('id')
    interaction = Interaction.query.get(interaction_id)
    note = interaction.note
    return note.text


################################################################################
# routes to get and post REMINDERS

@app.route('/getReminders.json', methods=['POST'])
def calculate_reminders():
    """calculates reminders to show"""

    # gets current user's id from session
    user_id = session['logged_in_user_id']

    # initializes a dictionary to store reminder information to pass to html
    reminders = {}

    # calculates which contacts are overdue for an interaction for a user
    # appents contact names and days overdue to a dictionary to pass to html
    contacts = db.session.query(Contact).filter(Contact.user_id == user_id).all()
    for c in contacts:
        update_t_since_last_int(c.contact_id)
        interactions = db.session.query(Interaction).filter(Interaction.contact_id == c.contact_id).all()
        days_overdue = round(c.t_since_last_int - c.avg_t_btwn_ints, 0)
        if (days_overdue > 0) and len(interactions) > 2:
            reminders[c.contact_id] = {
                'first_name': c.first_name,
                'last_name': c.last_name,
                'days_overdue': days_overdue
            }

    return jsonify(reminders)


################################################################################
# Runs app (with debugger tools)

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
