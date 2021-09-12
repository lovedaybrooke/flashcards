#!flask/bin/python
# -*- coding: utf-8 -*-

import os
import unittest

from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy

from config import basedir
from app.models import *
from . import factories as factories



class TestLearner(TestCase):

    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'
                  ] = 'postgresql://localhost/flashcards_testing'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        return app

    def setUp(self):
        db.create_all()
        factories.create_objects_for_testing(db)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_or_find(self):
        existing_learner = Learner.create_or_find("Nigel")
        self.assertEqual(existing_learner.id,1)
        not_yet_made_learner = Learner.query.filter_by(name = "Jem").all()
        self.assertFalse(not_yet_made_learner)
        new_learner = Learner.create_or_find("Jem")
        self.assertEqual(new_learner.id,2)

if __name__ == '__main__':
    unittest.main()
