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

class TestCombinations(TestCase):

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

    def test_all_combos_present(self):
        should_be = ['cat-eat: seafood', 'cat-go: sidle', 'cat-make: ignore',
                     'cat-see: ignore', 'dog-eat: meat', 'dog-make: create',
                     'dog-see: polarise', 'fish-eat: seafood']
        self.assertEqual(should_be, 
                         sorted([str(c) for c in Combination.query.all()]))

    def test_get_wrong_meaning(self):
        c = Combination.query.get(5)
        self.assertEqual(str(c), 'cat-see: ignore')
        c2 = c.get_wrong_meaning()
        self.assertTrue(c2["text"] != 'ignore')

    def test_get_wrong_stem(self):
        c = Combination.query.get(1)
        self.assertEqual(str(c), 'dog-make: create')
        c2 = c.get_wrong_stem()
        self.assertEqual(c2["wrong_answer"][:3],'dog')
        self.assertFalse(c2["wrong_answer"][3:] == 'make')
        c2_meaning = VerbMeaning.query.get(
                        Combination.query.get(c2["stem_id"]).meaning_id
                        ).append_hint()
        self.assertFalse(c2_meaning == 'create')

    def test_get_wrong_prefix(self):
        c = Combination.query.get(6)
        self.assertEqual(str(c), 'cat-eat: seafood')
        c2 = c.get_wrong_prefix()
        self.assertEqual(c2["wrong_answer"][3:],'eat')
        self.assertFalse(c2["wrong_answer"][:3] == 'cat')
        self.assertEqual('meat', 
                         Combination.get_meaning_from_verb(c2["wrong_answer"]))



if __name__ == '__main__':
    unittest.main()
