"""Helper functions for server.py"""

from model import connect_to_db, db, User, Interaction, Contact, Note
import datetime


def sort_user_interactions_by_date(user_id):
    """returns a list of interactions for a user, sorted by most recent first"""

    # returns the user object to be able to display their profile information
    user = User.query.get(user_id)

    # returns a list of interactions by the current user, newest first
    user_interactions = db.session.query(Interaction).filter(Interaction.user_id == user_id)
    user_interactions = sorted(user_interactions, key=lambda i: i.date, reverse=True)

    # formats the date as a readable string
    ints_with_dates = []
    for interaction in user_interactions:
        date = interaction.date.strftime('%A, %b %d')
        ints_with_dates.append((interaction, date))

    return ints_with_dates


def get_and_sort_contacts_by_power(user_id):
    """gets all contacts of a user, calculates their power, and returns a tuple
    with contact's power as a percent of max power"""

    # returns a list of contact objects for the given user
    user_contacts = db.session.query(Contact).filter(Contact.user_id == user_id).all()

    # creates a list of tuples to store (power-%, fname, lname, contact_id) and sorts by power
    contact_powers = []
    if user_contacts:
        for contact in user_contacts:
            power = calculate_power(contact.contact_id)
            contact_powers.append([power, contact.first_name, contact.last_name, contact.contact_id])
        contact_powers = sorted(contact_powers, reverse=True)

        # calculates power as a percentage of the largest power in the list
        max_power = contact_powers[0][0]
        for power in contact_powers:
            if max_power != 0:
                power[0] = (power[0] / max_power) * 100

    return contact_powers


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
    today = datetime.date.today()

    # sorts the list of interactions for the contact by date, newest first
    int_list = sorted(contact.interactions, key=lambda i: i.date, reverse=True)

    # updates the attribute by subtracting dates and converting to integer
    if int_list:
        delta = int_list[0].date - today
        delta = delta.days
        contact.t_since_last_int = abs(delta)
    else:
        contact.t_since_last_int = -1

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
