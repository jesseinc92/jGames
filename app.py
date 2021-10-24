import os
from threading import current_thread
from flask import Flask, render_template, redirect, flash, g, session
from models import db, db_connect, User, List, Game, List_Game

CURR_USER_KEY = 'current_user'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///jgames')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '135ace246')

db_connect(app)
db.create_all()



@app.before_request    
def add_user_to_g():
    '''Add session to global object'''
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        
    else:
        g.user = None

    
def do_login(user):
    '''Login user by adding user_id to session'''
    
    session[CURR_USER_KEY] = user.id


def do_logout():
    '''Logout user by removing user key from session'''

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]



@app.route('/')
def landing_page():
    '''The application homepage after signup/authentication'''
    
    if g.user:
        return 'This is the homepage.'
    
    else:
        return redirect('/login')
    
    

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    '''This view displays a login form'''
    
    return 'This is the login page (GET requests only)'



@app.route('/logout', methods=['POST'])
def logout_path():
    '''This view logs out the user and redirects to the root'''
    
    return redirect('/')
