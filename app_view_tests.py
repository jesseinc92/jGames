import os
from unittest import TestCase
from flask import g

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
            
            
            
            
class UserViewTest(TestCase):
    '''Test views relating to users.'''
    
    def setUp(self):
        
        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        
        self.test_user = User.signup(
            username='testuser',
            password='testuser',
            first_name='tester1',
            last_name='testington',
            avatar=None,
            bio=None
        )
        
        self.test_user_id = 101
        self.test_user.id = self.test_user_id
        
        db.session.commit()
    
    
    def tearDown(self):
        
        resp = super().tearDown()
        db.session.rollback()
        return resp
    
    
    def test_user_detail(self):
        with self.client as c:
            resp = c.get(f'/user/{self.test_user_id}')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 302)
            
            
    def test_user_detail_signed_in(self):
        
        with app.app_context():
            def get_user():
                g.user = self.test_user
        
                with self.client as c:
                    resp = c.get(f'/user/{self.test_user_id}')
                    html = resp.get_data(as_text=True)
                    
                    self.assertEqual(resp.status_code, 200)
                    self.assertIn('<div id="dashboard-list-preview">', html)
            
            
    def test_user_edit(self):
        with self.client as c:
            resp = c.get(f'/user/{self.test_user_id}')
            
            self.assertEqual(resp.status_code, 302)
            
            
    def test_user_edit_signed_in(self):
        
        with app.app_context():
            def get_user():
                g.user = self.test_user
                
                with self.client as c:
                    resp = c.get(f'/user/{self.test_user_id}/edit')
                    html = resp.get_data(as_text=True)
                    
                    self.assertEqual(resp.status_code, 200)
                    self.assertIn('<div id="edit-user-landing">', html)
                    
                    
                    
class ListViewTest(TestCase):
    '''Test views relating to lists'''
    
    def setUp(self):
        db.drop_all()
        db.create_all()

        self.client = app.test_client()
        
        self.list_id = 101
        
        self.test_user = User.signup(
            username='testuser',
            password='testuser',
            first_name='tester1',
            last_name='testington',
            avatar=None,
            bio=None
        )
        
        self.test_user_id = 101
        self.test_user.id = self.test_user_id
        
        db.session.commit()
        
        
    def tearDown(self):
        
        resp = super().tearDown()
        db.session.rollback()
        return resp
        
    
    def test_list(self):
        with self.client as c:
            resp = c.get(f'/lists/{self.list_id}')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div id="hero-list-details">', html)
            
            
    def test_list_new(self):
        
        with app.app_context():
            def get_user():
                g.user = self.test_user
        
                with self.client as c:
                    resp = c.get(f'/lists/{self.user_id}/new')
                    html = resp.get_data(as_text=True)    
                    
                    self.assertEqual(resp.status_code, 302)    
                    
                    
    def test_list_new_signed_in(self):
        
        with app.app_context():
            def get_user():
                user_id = self.test_user.id
                g.user = self.test_user
        
                with self.client as c:
                    resp = c.get(f'/lists/{self.user_id}/new')
                    html = resp.get_data(as_text=True)    
                    
                    self.assertEqual(resp.status_code, 200)
                    self.assertIn('<button class="button">Create List</button>', html)
                    
                    
    def test_list_edit(self):
        with self.client as c:
            resp = c.get(f'/lists/{self.list_id}/edit')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 302)
            
            
    def test_list_edit(self):
        
        with app.app_context():
            def get_user():
                g.user = self.test_user
        
                with self.client as c:
                    resp = c.get(f'/lists/{self.list_id}/edit')
                    html = resp.get_data(as_text=True)
                    
                    self.assertEqual(resp.status_code, 200)
                    self.assertIn('<button class="button">Save</button>', html)
                    
                    
    def test_list_delete(self):
        with self.client as c:
                    resp = c.get(f'/lists/{self.list_id}/delete')
                    html = resp.get_data(as_text=True)
                    
                    self.assertEqual(resp.status_code, 302)
                    
                    
    def test_list_delete(self):
        
        with app.app_context():
            def get_user():
                g.user = self.test_user
                
                with self.client as c:
                    resp = c.get(f'/lists/{self.list_id}/delete')
                    html = resp.get_data(as_text=True)
                    
                    self.assertEqual(resp.status_code, 302)
                    
            
    
class QueryViewTest(TestCase):
    '''Test views relating to queries'''
    
    def test_search(self):
        with app.test_client() as c:
            resp = c.get('/search')
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('<div id="search-results">', html)