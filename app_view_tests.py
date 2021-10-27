import os
from re import TEMPLATE
from unittest import TestCase

from werkzeug.utils import send_file
from models import db, db_connect, User, Game, List, List_Game

os.environ['DATABASE_URL'] = 'postgresql:///jgames-test'

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False



class LoginLogoutTest(TestCase):
    '''Test views for login/logout/signup'''
    
    def setUp(self):
        
        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        
        
    def tearDown(self):
        
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    
    def test_landing(self):
        with self.client as c:
            resp = c.get('/')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<ul class="navlink-wrapper">', html)
            
    
    def test_signup(self):
        with self.client as c:
            resp = c.get('/signup')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button class="button">Create Account</button>', html)
            
            
    def test_login(self):
        with self.client as c:
            resp = c.get('/login')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<button class="button">Login</button>', html)
            
            
    def test_logout(self):
        with self.client as c:
            resp = c.get('/logout')
            
            self.assertEqual(resp.status_code, 302)