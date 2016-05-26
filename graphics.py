"""Routes for creating graphics data"""

from model import connect_to_db, db, User, Interaction, Contact, Note
from flask import jsonify
import datetime
import random

COLORS = {"Periwinkle": "rgba(0, 0, 168, 0.6)",
          "Purple": "rgba(84, 0, 168, 0.6)",
          "Pink": "rgba(168, 0, 168, 0.6)",
          "Red": "rgba(168, 0, 0, 0.6)",
          "Green": "rgba(168, 0, 0, 0.6)",
          "Teal": "rgba(0, 168, 168, 0.6)",
          "Blue": "rgba(0, 84, 168, 0.6)",
          "lightPeriwinkle": "rgba(0, 0, 168, 0.3)",
          "lightPurple": "rgba(84, 0, 168, 0.3)",
          "lightPink": "rgba(168, 0, 168, 0.3)",
          "lightRed": "rgba(168, 0, 0, 0.3)",
          "lightGreen": "rgba(168, 0, 0, 0.3)",
          "lightTeal": "rgba(0, 168, 168, 0.3)",
          "lightBlue": "rgba(0, 84, 168, 0.3)",
          }


def get_frienergy_by_time(user_id):
    """ Bar chart """

    # generates a dictionary with all dates since first interaction as keys
    base = datetime.date.today()
    numdays = (base - Interaction.query.get(1).date).days
    frienergy_by_date = {}
    for num_days in range(0, numdays + 1):
        date = (base - datetime.timedelta(num_days)).strftime("%m-%d")
        frienergy_by_date[date] = []

    # gets all interactions of current user and adds a list of frienergies
    # by date into the dictionary.
    # Ex: frienergy_by_date = {"5-23": [3, 5, 7],...}
    all_interactions = db.session.query(Interaction).filter(Interaction
                                        .user_id == user_id).all()
    for interaction in all_interactions:
        date = interaction.date.strftime("%m-%d")
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
                "backgroundColor": "rgba(195, 189, 218, .4)",
                # "fillColor": "rgba(220,220,220,0.2)",
                # "strokeColor": "rgba(220,220,220,1)",
                # "pointColor": "rgba(220,220,220,1)",
                # "pointStrokeColor": "#fff",
                # "pointHighlightFill": "#fff",
                # "pointHighlightStroke": "rgba(220,220,220,1)",
                "data": total_frienergy_per_day
            },
            {
                "label": "Number of Interactions",
                "backgroundColor": "rgba(108, 100, 139, .4)",
                # "fillColor": "rgba(151,187,205,0.2)",
                # "strokeColor": "rgba(151,187,205,1)",
                # "pointColor": "rgba(151,187,205,1)",
                # "pointStrokeColor": "#fff",
                # "pointHighlightFill": "#fff",
                # "pointHighlightStroke": "rgba(151,187,205,1)",
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

    # calculates values as percentages of total number of interactions
    for x in range(1, 11):
        frienergies[x] = round((float(frienergies[x])/total_interactions)*100,0)

    # gets 10 colors from global COLORS dictionary
    colors = []
    for x in range(0, 10):
        colors.append(random.choice(COLORS.values()))

    # renders data readable for pie chart
    data_dict = {
        "labels": frienergies.keys(),
        "datasets": [
            {
                "data": frienergies.values(),
                "backgroundColor": colors
            }
        ],
    }

    return jsonify(data_dict)
