# Frienergy
#### By Allison Lyon, 2016
Frienergy is a contact management system for social connections. In addition to storing contact information, the app provides graphical representations of a user's social interactions and relationship health. 

Frienergy was inspired from a desire to develop depth and quality in social relationships. Frienergy achieves this goal by helping keep the friends that matter most at the forefront of the user's mind and by making sure a user doesn't lose track of friendships he/she considers most meaningful. 

## Table of Contents
* [Terminology](#terminology)
* [Technologies Used](#technologiesused)
* [Installation](#installation)
* [Features](#features)
* [Version 2.0](#version2)
* [Author](#author)

## <a name="terminology"></a>Terminology
#### Frienergy
Frienergy is an arbitrary unit a user can assign to the level of 'meaningfulness' of a social interaction. For example, a quick text message may only be valued at one unit of frienergy, whereas a weekend trip may receive a value of ten out of ten on the frienergy scale. 

It is important to note that all interactions are measured on a scale of 1-10 frienergy points, and all interactions can only have positive frienergy points. If a user feels an interaction was more negative than positive, they can simply chose not to keep track of interactions with that contact. There are no comparison's with other users. All ranking of interactions and assignment of frienergy points is kept personal, and is for the use of the user only. 

#### Pal-Power
Pal-Power is a unit used to quantify the health of a particular relationship. It is the rate of frienergy exchange with a contact, and is calculated as total frienergy divided by the total number of days that relationship has been tracked with the app. Contacts are displayed in order of Pal-Power, so the most meanintful relationships will always appear at the top of a user's contact list. 

## <a name="technologiesused"></a>Technologies Used
* HTML5/CSS3
* Javascript/
* [AJAX/JSON](http://www.json.org/)
* [AngularJS](https://angularjs.org/)
* [Jinja2](http://jinja.pocoo.org/docs/dev/)
* [Python](https://www.python.org/)
* [Flask](http://flask.pocoo.org/)
* [Bootstrap](http://getbootstrap.com/2.3.2/)
* [jQuery](https://jquery.com/)
* [Flask - SQLAlchemy](http://flask.pocoo.org/)
* [PostgresSQL](https://www.postgresql.org/)
* [Twilio API](https://www.twilio.com/)
* [Chart.js](http://www.chartjs.org/)

## <a name="installation"></a>Installation Instructions
1. Clone the repository locally: `$ git clone https://github.com/lyoness1/frienergy.git`
2. Create a virtual environment: `$ virtualenv env` 
3. Activate the virtual environment: `$ source env/bin/activate`
4. Install the dependencies: `(env)$ pip install -r requirements.txt`
5. Install and run the [PostgresApp](http://postgresapp.com/) 
6. Create a frienergy database: `(env)$ createdb frienergy`
7. Run the model interactively: `(env)$ python -i model.py`
8. Once inside the model, create the tables: `>>> db.create_all()`, then `>>> quit()`
9. Run the server: `(env)$ python server.py`
10. Navigate to <http://127.0.0.1:5000/> in a browser. 

## <a name="features"></a>Features
#### Login/Register
Frienergy provides a method to create individual accounts. Each user can store their own contacts and log their own interactions. Every user is provided with a unique dashboard that summarizes their realtionships and social interaction behavior. 

#### Dashboard View
Each Frienergy user is provided their own unique dashbaord view: 
![Dashbaord View](/static/images/screenshots/dashboard.png)
The dashboard summarizes a user's total number of contacts, interactions, and frienergy logged. The dashbaord also provides graphical visualization of their frienergy and interactions over time, as well as how many interactions were ranked at which levels of frienergy exchange. At the bottom of the dashboard, each user can see a list of their contacts along side their calculated pal-power for that contact, a lsit of their logged interactions, and reminders for which contacts need calculating. 

#### Add Contact
Frienergy provides a method to store contact information for every contact. By clicking on the <img src="/static/images/add_contact.png" width="24"> button on the 'Contacts' panel, users can easily add friends to their database: <img src="/static/images/screenshots/add-contact.png">

#### View/Edit Contact
By clicking on a contact's name, users are directed to a page displaying contact information for the contact, as well as relationship information regarding that contact only. All of the statistics from the dashboard are rendered using only that contact's interaction information from the databse. 

From within the contact view page, by clicking the <img src="/static/images/pencil.png" width="24"> icon under 'Edit contact', users can easily update contact information or delete a contact from the database. 

#### Add/Edit/Delete Interaction
Clicking on the <img src="/static/images/plus.png" width="24"> icon next to a contact's name, a user can easily add an interaction with that contact to the database. Interactions have a date, a frienergy value (integers from 1 to 10),  and the option of adding a note about the interaction. 

#### Notes
Each interaction has the option of having a note pinned to it. A note can be any information a user wants to store to remind themself about the interaction, or notes about the contact that they may want to remember for the next time they connect. Notes can be viewed by chosing the <img src="/static/images/Note.png" width="24"> icon from within the interactions panel. 

#### Get Reminders
One of the major features of Frienergy is the reminders panel. Frienergy automatically calculates the average number of days between interactions for each contact in the user's database. If too many days have elapsed from the last time the user connected with a certain contact, Frienergy will populate the reminders panel with that contact's name and how many days overdue an interaction is with them. 

#### Send Text Messages 
From within the reminders panel, Frienergy provides the option of sending a text message directly to a contact, if they have provided a phone number for that contact. Currently, in the demo version posted here, Frienergy is hard-coded to only send messages to one number to avoid paying for the Twilio API. Messages are sent by chosing the <img src="/static/images/sms.png" width="24"> icon from within the reminders panel. 

#### View Interactions Graphically by Varied Time Scales
From within the graphical display panel 'Frienergy by Date', users can chose what time frame from which they want to view their interaction and frienergy statistics. By chosing the default of 'All Time", interactions are displayed from the first use of the app. Time scales of the previous week or the previous month are also options: 
<img src="/static/images/screenshots/dashboard-graph.png">

## <a name="version2"></a>Version 2.0
In further versions of the app, features that could be added include: 
- Calendar view or heat map of interactions
- JavaScript validation on forms
- Ability to import contacts from social media, such as Facebook
- Ability to upload images for contacts
- Hashing passwords before storing in database
- Option to change skins with different css files to load

## <a name="author"></a>About Allison
Allison is a software engineer based in San Francisco, CA
