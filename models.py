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
        
        user = cls.query.filter_by(username=username).first()
        
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
    
    id = db.Column(db.String, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    release_date = db.Column(db.Text, default='Not listed')
    deck = db.Column(db.Text, default='Not listed')
    summary = db.Column(db.Text, default='Not listed')
    reviews = db.Column(db.Text, default='Not listed')
    main_image = db.Column(db.String, nullable=False)
    images = db.Column(db.ARRAY(db.String), default='None found')
    videos = db.Column(db.ARRAY(db.String), default='None found')
    platforms = db.Column(db.ARRAY(db.String), default='None found')
    dlc = db.Column(db.ARRAY(db.String), default='None found')
    
    @classmethod
    def create(cls, game):
        '''Utility method for creating a game row in db'''

        images_array = list()
        if game.get('images'):
            for img in game.get('images'):
                img_url = img.get('original')
                images_array.append(img_url)
        
        print(images_array)
            
        videos_array = list()
        if game.get('videos'):
            for vid in game.get('videos'):
                vid_api_url = vid.get('api_detail_url')
                videos_array.append(vid_api_url)
            
        print(videos_array)
            
        platforms_array = list()
        if game.get('platforms'):
            for pf in game.get('platforms'):
                platform = pf.get('name')
                platforms_array.append(platform)
            
        print(platforms_array)
            
        dlc_array = list()
        if game.get('dlcs'):
            for item in game.get('dlcs'):
                item_name = item.get('name')
                dlc_array.append(item_name)
        
        print(dlc_array)
        
        new_game = Game(
            id=game.get('guid'),
            title=game.get('name'),
            release_date=game.get('original_release_date') or Game.release_date.default.arg,
            deck=game.get('deck') or Game.deck.default.arg,
            summary=game.get('description') or Game.summary.default.arg,
            main_image=game.get('image').get('original_url'),
            images=images_array or Game.images.default.arg,
            videos=videos_array or Game.video.default.arg,
            platforms=platforms_array or Game.platforms.default.arg,
            dlc=dlc_array or Game.dlc.default.arg
        )
        
        db.session.add(new_game)
        return new_game
        
    
    
class List_Game(db.Model):
    '''A model that associates games with a list id to track what game has been added to what list'''
    
    __tablename__ = 'lists_games'
    
    list_id = db.Column(db.Integer, db.ForeignKey('lists.id'), primary_key=True)
    game_id = db.Column(db.String, db.ForeignKey('games.id'), primary_key=True)