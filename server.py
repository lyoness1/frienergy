"""Frienergy"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Contact, Interaction, Note



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
    db_user = db.session.query(User).filter(User.email==email).first()
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
        flash("No user registered with that email. " + \
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
    user_interactions = db.session.query(Interaction).filter(Interaction.user_id==user_id)
    user_interactions = sorted(user_interactions, key=lambda i: i.date, reverse=True)

    user_contacts = db.session.query(Contact).filter(Contact.user_id==user_id)

    return render_template("dashboard.html",
                           user=user,
                           interactions=user_interactions,
                           contacts=user_contacts)


@app.route('/interactions')
def show_interactions():
    """Lists the interactions of the current user"""
    pass


@app.route('/contacts')
def show_contacts():
    """SHows a list of contacts of the current user"""
    pass


@app.route('/contact/<int:contact_id>')
def detail_contact():
    """Shows the history of interactions for a specific relationship"""
    pass 



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
