from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.fields.core import SelectField
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
    
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    avatar = StringField('Avatar')
    bio = TextAreaField('Bio')
    
    
################ LIST FORMS ###################

class NewListForm(FlaskForm):
    '''A template for creating new lists'''
    
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    description = StringField('Description')
    
    
class EditListForm(FlaskForm):
    '''A template for editing lists'''
    
    name = StringField('Name', validators=[InputRequired(), Length(max=20)])
    description = StringField('Description')
    
    
class AddToListForm(FlaskForm):
    '''A template for adding a game to a list'''
    
    lists = SelectField('Lists', coerce=int)
    
    
############# QUERY / SEARCH FORMS ############

class GameSearch(FlaskForm):
    '''Template for main game search'''
    
    search = StringField('Search')