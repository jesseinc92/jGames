import os
from flask import Flask, render_template, redirect, flash, g, session
from sqlalchemy.exc import IntegrityError
from models import db, db_connect, User, List, Game, List_Game
from forms import LoginForm, SignupForm, EditUser, GameSearch

CURR_USER_KEY = 'current_user'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql:///jgames')
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', '135ace246')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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


# ---------- LOGIN / LOGOUT / SIGNUP ------------ #

@app.route('/')
def landing_page():
    '''The application homepage after signup/authentication'''
    
    if g.user:
        form = GameSearch()
        return render_template('index.html', form=form)
    
    else:
        return render_template('index.html')
    
    
    
@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    '''Displays a signup form for new users'''
    
    form = SignupForm()
    if form.validate_on_submit():
        try:
            
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                avatar=form.avatar.data or User.avatar.default.arg,
                bio=form.bio.data
            )
            
            db.session.commit()
            
        except IntegrityError:
            flash('Username already taken', 'danger')
            return render_template('/signup', form=form)
            
        do_login(user)
        
        return redirect('/')
    
    return render_template('signup.html', form=form)
    
    

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    '''This view displays a login form'''
    
    form = LoginForm()
    if form.validate_on_submit():
        
        username = form.username.data
        password = form.password.data
        
        user = User.authenticate(username, password)
        if user:
            do_login(user)
            return redirect('/')
        
        else:
            return render_template('login.html', form=form)
    
    return render_template('login.html', form=form)



@app.route('/logout')
def logout_path():
    '''This view logs out the user and redirects to the root'''
    
    do_logout()
    return redirect('/')

# ----------------------------------------------- #


# -------------------- USER --------------------- #

@app.route('/user/<int:user_id>')
def user_dashboard(user_id):
    '''This view displays an individual user's dashboard'''
    
    if g.user:
        user = User.query.get(user_id)
        return render_template('user/dashboard.html', user=user)
    
    else:
        return redirect('/')
    
    

@app.route('/user/<int:user_id>/edit', methods=['GET', 'POST'])
def user_lists(user_id):
    '''Shows a page that allows a user to edit their details'''
    
    user = User.query.get(user_id)
    if g.user.id == user.id:
    
        form = EditUser(obj=user)
        if form.validate_on_submit():
            
            # capture form data and update user properties
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.avatar = form.avatar.data or User.avatar.default.arg
            user.bio = form.bio.data
            
            db.session.commit()
            
            return redirect(f'/user/{user_id}')
    
        return render_template('user/edit.html', form=form)
    
    else:
        return redirect('/')

# ----------------------------------------------- #


# ------------------ LISTS ---------------------- #

@app.route('/lists/<int:list_id>')
def show_list(list_id):
    '''Displays a list and its contents'''
    
    

@app.route('/lists/<int:user_id>/new')
def new_list(user_id):
    '''Displays a page that allows you to create a new list'''
    
    

@app.route('/lists/<int:list_id>/edit')
def edit_list(list_id):
    '''Allows a user to edit the details of a list and its contents'''
    
    

@app.route('/lists/<int:list_id>/delete')
def delete_list(list_id):
    '''Deletes a list'''

# ----------------------------------------------- #

# ------------------ QUERIES -------------------- #

@app.route('/search')
def search_for_games():
    '''Displays the search landing page'''

# ----------------------------------------------- #