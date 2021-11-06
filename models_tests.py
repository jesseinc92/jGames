import os
from sys import platform
from unittest import TestCase
from flask import g
from werkzeug import test
from models import db, db_connect, User, Game, List, List_Game

os.environ['DATABASE_URL'] = 'postgresql:///jgames-test'

from app import app, CURR_USER_KEY

app.config['WTF_CSRF_ENABLED'] = False



class UserModelTest(TestCase):
    
    def setUp(self):
        '''Create test client, add sample data'''
        db.drop_all()
        db.create_all()
        
        u1 = User.signup("test1", "password", 'tester', 'mctester', None, 'test_bio')
        uid1 = 1111
        u1.id = uid1

        u2 = User.signup('test2', 'password', 'tester2', 'mctester2', None, 'test_bio_2')
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()
        
        
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    
    def test_user_model(self):
        user = User(
            username='test',
            password='hashed_pwd',
            first_name='fname',
            last_name='lname',
            avatar=None,
            bio='test_bio'
        )

        db.session.add(user)
        db.session.commit()
        
        self.assertEqual('test', user.username)
        self.assertEqual('fname', user.first_name)
        self.assertEqual('lname', user.last_name)
        self.assertEqual('test_bio', user.bio)
        
        
    def test_user_signup(self):
        
        self.assertEqual('test1', self.u1.username)
        self.assertEqual('tester', self.u1.first_name)
        self.assertEqual('mctester', self.u1.last_name)
        
        self.assertEqual('test2', self.u2.username)
        self.assertEqual('tester2', self.u2.first_name)
        self.assertEqual('mctester2', self.u2.last_name)
        
        
        
class ListModelTest(TestCase):
    
    def setUp(self):
        '''Create test client, add sample data'''
        db.drop_all()
        db.create_all()
        
        u1 = User.signup("test1", "password", 'tester', 'mctester', None, 'test_bio')
        uid1 = 1111
        u1.id = uid1
        
        db.session.commit()

        u1 = User.query.get(uid1)
        self.u1 = u1
        self.uid1 = uid1
        
        self.client = app.test_client()
        
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    
    def test_list_model(self):
        
        test_list = List(
            name='favorites',
            description='tests_description',
            user_id=self.u1.id
        )
        
        db.session.add(test_list)
        db.session.commit()
        
        
        self.assertEqual('favorites', test_list.name)
        self.assertEqual(len(test_list.game), 0)
        
        
        
class GameModelTest(TestCase):
    
    def setUp(self):
        self.game = {
            "description": "test_summary",
            "guid": "3030-17280",
            "image":
                {
                "original_url": "https://www.giantbomb.com/a/uploads/original/8/82063/2584146-bioshock.jpg",
                },
            "name": "BioShock",
            "original_release_date": "2007-08-21",
            "platforms": [
                {
                    "name": "Mac"
                },
                {
                    "name": "Xbox 360"
                },
                {
                    "name": "iPad"
                }
            ],
            "images": [
                {
                    
                    "original": "https://www.giantbomb.com/a/uploads/original/46/468536/3210717-1%20%2847%29.jpg"
                },
                {
                    "original": "https://www.giantbomb.com/a/uploads/original/46/468536/3210716-1%20%2846%29.jpg"
                },
                {
                    "original": "https://www.giantbomb.com/a/uploads/original/46/468536/3210685-1%20%283%29.jpg"
                }
            ],
            "videos": [
                {
                    "api_detail_url": "https://www.giantbomb.com/api/video/2300-5/",
                },
                {
                    "api_detail_url": "https://www.giantbomb.com/api/video/2300-45/"
                }
            ]
        }
        
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    
    def test_game_create(self):
        
        self.test_game = Game.create(self.game)
        
        db.session.add(self.test_game)
        db.session.commit()
        
        
        self.assertEqual('BioShock', self.test_game.title)
        self.assertEqual([
            'https://www.giantbomb.com/api/video/2300-5/',
            'https://www.giantbomb.com/api/video/2300-45/'
            ],
                         self.test_game.videos)