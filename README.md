# loginregister

Installation

Create a virtual environment 
# to start in terminal
Pip install flask 
(pip install- windows , pip3 install-mac)
#Install flask to your chosen platform for python 

pip install Flask-Login
pip install SQLAlchemy
pip install Flask-WTF
pip install WTForms
pip install wtforms-validators
pip install Flask-Bcrypt

Import flask, render template, url for, redirect
Python app.py

Creating database
#when creating the database- python app.py in terminal add

from app import app
db = app.extensions['sqlalchemy']
with app.app_context():
    db.create_all() (with tab)


Usage 

python app.py (windows)
python3 app.py (Mac)
