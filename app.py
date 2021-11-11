import os
from flask import Flask, render_template, redirect, flash, g, session
from sqlalchemy.exc import DatabaseError, IntegrityError, ProgrammingError
from werkzeug.wrappers import response
from models import db, db_connect, User, List, Game, List_Game
from forms import LoginForm, SignupForm, EditUser, GameSearch, NewListForm, EditListForm, AddToListForm
from api_helpers import game_query, search_query, video_query


CURR_USER_KEY = 'current_user'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///jgames') #.replace("://", "ql://", 1) # os.environ.get('DATABASE_URL', 'postgresql:///jgames')
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
            flash('Username is already in use.', 'danger')
            return render_template('signup.html', form=form)
            
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
            flash('There was a problem with your username or password.', 'danger')
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
    
    game_list = List.query.get(list_id)
    
    return render_template('list/list.html', list=game_list)
    
    

@app.route('/lists/<int:user_id>/new', methods=['GET', 'POST'])
def new_list(user_id):
    '''Displays a page that allows you to create a new list'''
    
    if g.user.id == user_id:
        user = User.query.get(user_id)
        
        form = NewListForm()
        if form.validate_on_submit():
            name = form.name.data
            description = form.description.data or List.description.default.arg
            list_user_id = user_id
            
            try:
            
                new_list = List(name=name, description=description, user_id=list_user_id)
            
                db.session.add(new_list)
                db.session.commit()
                
            except:
                flash('There was a problem creating your list!', 'danger')
                return render_template('list/new-list.html', form=form, user=user)    
            
            return redirect(f'/user/{user_id}')
    
        return render_template('list/new-list.html', form=form, user=user)
    
    else:
        return redirect('/')
    
    

@app.route('/lists/<int:list_id>/edit', methods=['GET', 'POST'])
def edit_list(list_id):
    '''Allows a user to edit the details of a list and its contents'''
    
    if g.user:
        
        list_det = List.query.get(list_id)
        form = EditListForm(obj=list_det)
        if form.validate_on_submit():
            
            list_det.name = form.name.data
            list_det.description = form.description.data or List.description.default.arg
            db.session.commit()
            
            return redirect(f'/lists/{list_id}')
        
        return render_template('list/edit-list.html', form=form, list=list_det)
    
    return redirect('/')
    
    

@app.route('/lists/<int:list_id>/delete')
def delete_list(list_id):
    '''Deletes a list'''
    
    if g.user:
        delete_list = List.query.get(list_id)
        db.session.delete(delete_list)
        db.session.commit()
    
        return redirect('/')
    
    return redirect('/')

# ----------------------------------------------- #

# ------------------- GAMES --------------------- #

@app.route('/games/<game_id>')
def game_details(game_id):
    '''Shows a page that displays an individual game's details'''
    
    game_resp = game_query(game_id)
    results = game_resp.get('results', 'No results found')
    
    return render_template('game/game-detail.html', game=results)



@app.route('/games/video/<video_id>')
def game_video_player(video_id):
    '''Displays a page where the video is embeded and played from API resource'''
    
    response = video_query(video_id)
    video = response.get('results')

    return render_template('game/video.html', video=video)



@app.route('/games/<game_id>/add', methods=['GET', 'POST'])
def list_game_add(game_id):
    '''Shows a form that processes which list to add the chosen game'''
    
    if g.user:
        
        form = AddToListForm()
        
        lists = [(li.id, li.name) for li in List.query.all()]
        form.lists.choices = lists
        
        if form.validate_on_submit():
            
            result = game_query(game_id)
            game = result.get('results')
            
            # check to see if game is already in db.
            # if not, create new game row.
            game_in_db = Game.query.get(game.get('guid'))
            
            if not game_in_db:
            
                try:
                    new_game = Game.create(game)
                    
                    if new_game:
                        db.session.commit()   
                        
                except:
                    flash('There was a problem adding your game!', 'danger')
                    return render_template('game/add-to-list.html', form=form)
            
            
            # collect form info and use it to create new list_game primary key
            list_id = form.lists.data
            
            new_list_game = List_Game(list_id=list_id, game_id=game_id)
            
            db.session.add(new_list_game)
            db.session.commit()
            
            return redirect(f'/lists/{list_id}')
    
        return render_template('game/add-to-list.html', form=form)
    
    return redirect('/')



@app.route('/games/<game_id>/<int:list_id>/delete', methods=['POST'])
def delete_game(game_id, list_id):
    '''Deletes a game from a list'''
    
    if g.user:
        list_game = List_Game.query.get((list_id, game_id))
        db.session.delete(list_game)
        db.session.commit()
    
        return redirect(f'/lists/{list_id}')
    
    return redirect('/')

# ----------------------------------------------- #

# ------------------- SEARCH -------------------- #

@app.route('/search', methods=['GET', 'POST'])
def search_for_games():
    '''Displays the search landing page'''
    
    form = GameSearch()
    if form.validate_on_submit():
        
        # send query string to request def
        search = form.search.data
        resp = search_query(search)
        
        results = resp.get('results', 'No results found')
        
        return render_template('game/search.html', form=form, results=results)
    
    return render_template('game/search.html', form=form)

# ----------------------------------------------- #