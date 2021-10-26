from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


############ USER FORMS ###############

class LoginForm(FlaskForm):
    '''Template for a login form object'''
    
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    
    
class SignupForm(FlaskForm):
    '''Template for a signup form object'''
    
    username = StringField('Username', validators=[InputRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    avatar = StringField('Avatar')
    bio = TextAreaField('Bio')
    
    
class EditUser(FlaskForm):
    '''Template for updating a specific user'''
    
    fist_name = StringField('First Name')
    last_name = StringField('Last Name')
    bio = TextAreaField('Bio')
    
    
############# QUERY / SEARCH FORMS ############

class GameSearch(FlaskForm):
    '''Template for main game search'''
    
    search = StringField('Search')