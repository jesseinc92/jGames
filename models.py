from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt()
db = SQLAlchemy()


def db_connect(app):
    '''Connects database to app'''
    
    db.app = app
    db.init_app(app)
    
    
class User(db.Model):
    '''A user model for user properties and methods'''
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    avatar = db.Column(db.Text, default='https://png.pngitem.com/pimgs/s/508-5087236_tab-profile-f-user-icon-white-fill-hd.png')
    bio = db.Column(db.Text)
    
    @classmethod
    def signup(cls, username, password, first_name, last_name, avatar, bio):
        '''Completes new user signup'''
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        
        user = User(
            username=username,
            password=hashed_pwd,
            first_name=first_name,
            last_name=last_name,
            avatar=avatar,
            bio=bio
        )
        
        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        '''Method to validate username/password'''
        
        user = cls.filter_by(username=username).first()
        
        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            
            if is_auth:
                return user
            
        return False
    


class List(db.Model):
    '''A list model for list properties and methods'''
    
    __tablename__ = 'lists'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    description = db.Column(db.Text, default='A list of some of my favorite games!')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship('User', backref='lists')
    game = db.relationship('Game', secondary='lists_games', backref='lists')
    
    
    
class Game(db.Model):
    '''A game model for saving game properties from API data and methods'''
    
    __tablename__ = 'games'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text, default='Not listed')
    summary = db.Column(db.Text, default='Not listed')
    reviews = db.Column(db.Text, default='Not listed')
    main_image = db.Column(db.Text, nullable=False)
    images = db.Column(db.Text, default='None found')
    videos = db.Column(db.Text, default='None found')
    plaforms = db.Column(db.Text, default='None found')
    dlc = db.Column(db.Text, default='None found')
    
    
    
class List_Game(db.Model):
    '''A model that associates games with a list id to track what game has been added to what list'''
    
    __tablename__ = 'lists_games'
    
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.id'), primary_key=True)