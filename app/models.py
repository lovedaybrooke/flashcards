#!flask/bin/python
# -*- coding: utf-8 -*-

import random
import datetime

from app import app, db


class Learner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    last_seen = db.Column(db.Date)

    @classmethod
    def create_or_find(cls, submitted_name):
        existing_learner = cls.query.filter_by(name=submitted_name).first()
        if existing_learner:
            existing_learner.last_seen = datetime.datetime.today()
            db.session.add(existing_learner)
            db.session.commit()
            return existing_learner
        else:
            new_learner = cls(name=submitted_name,
                              last_seen=datetime.datetime.today())
            db.session.add(new_learner)
            db.session.commit()
            return new_learner
