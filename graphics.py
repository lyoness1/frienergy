"""Routes for creating graphics data"""

from model import connect_to_db, db, User, Interaction, Contact, Note
from flask import jsonify
import datetime
import random

COLORS = ['rgba(209, 249, 210, .5)', 'rgb(209, 249, 210)', 'rgb(164, 243, 165)',
          'rgb(118, 238, 120)', 'rgb(73, 232, 76)', 'rgb(40, 182, 44)',
          'rgb(22, 181, 25)', 'rgb(16, 136, 18)', 'rgb(11, 90, 12)',
          'rgb(5, 45, 6)']


################################################################################
# FOR USER'S DASHBOARD PAGE

def get_frienergy_by_time(user_id, scale):
    """ Bar chart """

    # generates a dictionary with all dates as keys based on the given scale
    # values are initialized as empty lists that will store interaction data
    base = datetime.date.today()
    if scale == 'all-time':
        numdays = (base - Interaction.query.get(1).date).days
    elif scale == 'month':
        numdays = 30
    elif scale == 'week':
        numdays = 7
    frienergy_by_date = {}
    for num_days in range(0, numdays + 1):
        date = (base - datetime.timedelta(num_days)).strftime("%m-%d-%y")
        frienergy_by_date[date] = []

    # gets all interactions of current user and adds a list of frienergies
    # by date into the dictionary.
    # Ex: frienergy_by_date = {"5-23": [3, 5, 7],...}
    all_interactions = db.session.query(Interaction).filter(Interaction
                                        .user_id == user_id).all()
    for interaction in all_interactions:
        date = interaction.date.strftime("%m-%d-%y")
        if date in frienergy_by_date:
            frienergy_by_date[date].append(interaction.frienergy)

    keys = sorted(frienergy_by_date.keys())

    # makes two sets of data:
    # counts the number of interactions per date in the dictionary (Ex: 3)
    # counts the total amount of frienergy per date in the dictionary (Ex: 15)
    number_of_ints_per_day = []
    total_frienergy_per_day = []
    for key in keys:
        number_of_ints_per_day.append(len(frienergy_by_date[key]))
        total_frienergy_per_day.append(sum(frienergy_by_date[key]))

    data_dict = {
        "labels": keys,
        "datasets": [
            {
                "label": "Total Frienergy",
                "backgroundColor": "rgba(40, 182, 44, .5)",
                "data": total_frienergy_per_day
            },
            {
                "label": "Number of Interactions",
                "backgroundColor": "rgb(40, 182, 44)",
                "data": number_of_ints_per_day
            }
        ],
    }

    return jsonify(data_dict)

def get_frienergy_totals(user_id):
    """Returns number of interactions per amount of frienergy"""

    # gets all user's interactions from db
    all_interactions = db.session.query(Interaction).filter(Interaction
                                        .user_id == user_id).all()

    # calculates total number of interactions for user later in calculating %
    total_interactions = len(all_interactions)

    # creates a dictionary with frienergies 1-10 as keys and counts as values
    frienergies = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    # sums up the number of frienergies over all the interactions
    for interaction in all_interactions:
        frienergies[interaction.frienergy] += 1

    # renders data readable for pie chart
    data_dict = {
        "labels": frienergies.keys(),
        "datasets": [
            {
                "data": frienergies.values(),
                "backgroundColor": COLORS,
            }
        ],
    }

    return jsonify(data_dict)


################################################################################
# FOR USER'S CONTACT PAGES

def get_frienergy_by_time_for_contact(user_id, contact_id, scale):
    """ Bar chart """

    # generates a dictionary with all dates as keys based on the given scale
    # values are initialized as empty lists that will store interaction data
    base = datetime.date.today()
    first_interaction = db.session.query(Interaction).filter(Interaction.
                        contact_id == contact_id).first()
    if scale == 'all-time':
        numdays = (base - first_interaction.date).days
    elif scale == 'month':
        numdays = 30
    elif scale == 'week':
        numdays = 7
    frienergy_by_date = {}
    for num_days in range(0, numdays + 1):
        date = (base - datetime.timedelta(num_days)).strftime("%m-%d")
        frienergy_by_date[date] = []

    # gets all interactions of current user and adds a list of frienergies
    # by date into the dictionary.
    # Ex: frienergy_by_date = {"5-23": [3, 5, 7],...}
    all_interactions = db.session.query(Interaction).filter(Interaction
        .user_id == user_id).filter(Interaction.contact_id == contact_id).all()
    for interaction in all_interactions:
        date = interaction.date.strftime("%m-%d")
        if date in frienergy_by_date:
            frienergy_by_date[date].append(interaction.frienergy)

    keys = sorted(frienergy_by_date.keys())

    # makes two sets of data:
    # counts the number of interactions per date in the dictionary (Ex: 3)
    # counts the total amount of frienergy per date in the dictionary (Ex: 15)
    number_of_ints_per_day = []
    total_frienergy_per_day = []
    for key in keys:
        number_of_ints_per_day.append(len(frienergy_by_date[key]))
        total_frienergy_per_day.append(sum(frienergy_by_date[key]))

    data_dict = {
        "labels": keys,
        "datasets": [
            {
                "label": "Total Frienergy",
                "backgroundColor": "rgba(40, 182, 44, .5)",
                "data": total_frienergy_per_day
            },
            {
                "label": "Number of Interactions",
                "backgroundColor": "rgb(40, 182, 44)",
                "data": number_of_ints_per_day
            }
        ],
    }

    return jsonify(data_dict)


def get_frienergy_totals_for_contact(user_id, contact_id):
    """Returns number of interactions per amount of frienergy"""

    # gets all user's interactions from db
    all_interactions = db.session.query(Interaction).filter(Interaction
        .user_id == user_id).filter(Interaction.contact_id == contact_id).all()

    # calculates total number of interactions for user later in calculating %
    total_interactions = len(all_interactions)

    # creates a dictionary with frienergies 1-10 as keys and counts as values
    frienergies = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    # sums up the number of frienergies over all the interactions
    for interaction in all_interactions:
        frienergies[interaction.frienergy] += 1

    # renders data readable for pie chart
    data_dict = {
        "labels": frienergies.keys(),
        "datasets": [
            {
                "data": frienergies.values(),
                "backgroundColor": COLORS,
            }
        ],
    }

    return jsonify(data_dict)
