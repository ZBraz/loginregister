from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

# Create and configure the Flask application
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SECRET_KEY'] = 'Stockmarketgame'
    with app.app_context():
        
 # Create the database and tables 
        db.init_app(app)
        db.create_all()
        
    return app


db = SQLAlchemy()
app = create_app()
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#app = Flask(__name__)
#database instance
#connects app file to databse
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
#app.config['SECRET_KEY'] = 'stockmarketgame'

#db = SQLAlchemy(app)

# Define the User class as a SQLAlchemy model
#Three column table
class User(db.Model, UserMixin):
    #user identity column
    id = db.Column(db.Integer, primary_key=True)
    #username max 20 characters unique and cannot be left empty
    username = db.Column(db.String(20), nullable=False, unique=True)
    #password max 80 characters and connot be left empty
    password = db.Column(db.String(80), nullable=False)

    
# Define the registration form using FlaskForm
class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    
 # Validate the form data
    def validate_username(self, username):
        app.logger.debug('Trying to validate')
        existing_user_username = User.query.filter_by(
            username=self.username.data).first()
        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')

            
# Define the login form using FlaskForm            
class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')



@app.route('/')
def home():
    return render_template('HTML.html')


@app.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    #Retrieve the user from the database based on the entered username
    if form.validate_on_submit() and request.method == 'POST':
        user = User.query.filter_by(username=form.username.data).first()
         # Check if the entered password matches the stored hashed password
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
    return render_template('login.html', form=form)

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    # Log out the user using Flask-Login
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    app.logger.debug(form.validate_on_submit())
    app.logger.debug(form.validate())
    if form.validate_on_submit():
        # Generate a hash of the password using Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        # Create a new user in the database
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
