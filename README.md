
# purpose

Login system that allows users to register to create user name and password that are saved to a data base allowing accounts to be made for website login



# loginregister

Installation

Create a virtual environment 
# to start in terminal
Pip install flask 
(pip install- windows , pip3 install-mac)
#Install flask to your chosen platform for python 


Import flask, render template, url for, redirect
Python app.py

Creating database
#when creating the database- python app.py in terminal add

from app import app
-db = app.extensions['sqlalchemy']
-with app.app_context():
-(tab)    db.create_all() 


Usage 

python app.py (windows)
python3 app.py (Mac)
