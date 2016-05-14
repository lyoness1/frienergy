"""Frienergy"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Contact, Interaction, Note

import datetime


app = Flask(__name__)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


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
    session['logged_in_email'] = email
    session['logged_in_user_id'] = new_user.user_id
    session['logged_in_user_name'] = new_user.first_name
    flash("You have Successfully registred! You are now logged in.")
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


@app.route('/dashboard/<int:user_id>')
def show_dashboard(user_id):
    """Shows the dashboard for the current user"""

    # returns the user object to be able to display their profile information
    user = User.query.get(user_id)

    # returns a list of interactions by the current user, newest first
    user_interactions = db.session.query(Interaction).filter(Interaction.user_id == user_id)
    user_interactions = sorted(user_interactions, key=lambda i: i.date, reverse=True)

    # returns a list of contact objects for the given user
    user_contacts = db.session.query(Contact).filter(Contact.user_id == user_id)

    # creates a list of tuples to store (power, fname, lname, contact_id) and sorts by power
    contact_powers = []
    for contact in user_contacts:
        power = calculate_power(contact.contact_id)
        contact_powers.append((power, contact.first_name, contact.last_name, contact.contact_id))
    contact_powers = sorted(contact_powers, reverse=True)

    return render_template("dashboard.html",
                           user=user,
                           interactions=user_interactions,
                           contacts=contact_powers)


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

# FIXME #can't instantiate interaction unless Note obj exists as list object.
# How can I do this and pass "None" when creating an interaction instance?
    # gets note as string and converts to note object
    text = request.form.get('notes')
    new_note = Note(contact_id=contact_id,
                    text=text)

    # creates an interaction instance for the contact and adds it to the db
    new_interaction = Interaction(user_id=user_id,
                                  contact_id=contact_id,
                                  date=date,
                                  frienergy=frienergy,
                                  note=[new_note])
    db.session.add(new_interaction)
    db.session.commit()

    # calculates the *Interaction* attributes (plural): time since last interaction
    # can only be called after instantiating new interaction; order may be wrong
    calculate_t_delta_since_last_int(contact_id)

    # update all necessary contact attributes with new interaction data
    update_avg_t_btwn_ints(contact_id)
    update_total_frienergy(contact_id)

    # provides user feedback that interaction has been added
    flash("Interaction successfully added.")

    return redirect("/dashboard/"+str(user_id))


################################################################################
# Helper functions


def calculate_t_delta_since_last_int(contact_id):
    """updates the *Interaction* attributes (plural): time since last interaction"""

    # returns a list of all interactions on contact sorted by date, oldest first
    int_list = db.session.query(Interaction).filter(Interaction.contact_id == contact_id).all()
    int_list = sorted(int_list, key=lambda i: i.date)

    # calculates time between each interaction and reassigns attribute. 
    if len(int_list) > 1:
        for n in range(1, len(int_list)):
            delta = int_list[n].date - int_list[n-1].date
            int_list[n].t_delta_since_last_int = abs(int(delta.days))
    int_list[0].t_delta_since_last_int = 0


    # commit changes to db
    db.session.commit()


def update_t_since_last_int(contact_id):
    """calculates the *Contact* attribute (singular): time since last interaction"""

    # gets contact object from their id
    contact = Contact.query.get(contact_id)

    # gets a datetime date object for today
    today = datetime.date.today() # datetime.date(2016, 5, 13)
    
    # sorts the list of interactions for the contact by date, newest first
    int_list = sorted(contact.interactions, key=lambda i: i.date, reverse=True)

    # updates the attribute by subtracting dates and converting to integer
    delta = int_list[0].date - today
    contact.t_since_last_int = int(abs(delta))

    # commit calculation to database
    db.session.commit()

def update_total_frienergy(contact_id):
    """updates contact attributes: total_frienergy, avg_t_btwn_ints, and t_since_last_int"""

    # gets contact object from their id
    contact = Contact.query.get(contact_id)

    # calculates total frienergy for the contact by looping through int objs
    total_frienergy = 0
    interactions = contact.interactions
    for i in interactions:
        total_frienergy += i.frienergy

    # sets the attribute to the contact in the db
    contact.total_frienergy = float(total_frienergy)

    # commit changes to db
    db.session.commit()


def update_avg_t_btwn_ints(contact_id):
    """calculates average time between interactions for contact"""

    # gets contact object from their id
    contact = Contact.query.get(contact_id)

    # makes a list of contact's interactions, sorted with oldest int first
    int_list = contact.interactions
    int_list = sorted(int_list, key=lambda i: i.date)

    # makes a list to store all the time deltas between interactions
    deltas = []

    # calculates the average of the time deltas
    # if only one interaction, avg time delta is 0
    for i in int_list[1:]:
        deltas.append(i.t_delta_since_last_int)
    if deltas:
        contact.avg_t_btwn_ints = float(sum(deltas)) / (len(deltas))
    else:
        contact.avg_t_btwn_ints = 0

    # commit changes to db
    db.session.commit()


def calculate_power(contact_id):
    """calculates the power of a friendship as (total frienergy)/(avg interaction time-delta)"""

    # gets contact object from their id
    contact = Contact.query.get(contact_id)
    
    # gets current attributes of total frienergy and avg time delta between ints
    frienergy = contact.total_frienergy
    avg_t_btwn_ints = contact.avg_t_btwn_ints
    
    # calcualtes and returns relationship power
    if avg_t_btwn_ints != 0:
        return round(frienergy / avg_t_btwn_ints, 1)
    else:
        return 0


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
