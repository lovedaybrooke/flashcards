#!flask/bin/python
# -*- coding: utf-8 -*-

import random
import datetime

from app import app, db


class VerbStem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stem = db.Column(db.Text)


class VerbPrefix(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.Text)


class VerbMeaning(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meaning = db.Column(db.Text)
    hint = db.Column(db.Text)


class Combination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix_id = db.Column(db.Integer, db.ForeignKey('verb_prefix.id'))
    stem_id = db.Column(db.Integer, db.ForeignKey('verb_stem.id'))
    meaning_id = db.Column(db.Integer, db.ForeignKey('verb_meaning.id'))

    def get_learning_info(self, question_type):
        prefix = VerbPrefix.query.filter_by(id=self.prefix_id).first()
        stem = VerbStem.query.filter_by(id=self.stem_id).first()
        meaning = VerbMeaning.query.filter_by(
                            id=self.meaning_id).first()
        if meaning.hint:
            meaning = meaning.meaning + " " + meaning.hint
        else:
            meaning = meaning.meaning
        if question_type == "different_prefix":
            return {"question_type": question_type,
                    "combination_id": self.id,
                    "right_answer": prefix.prefix+stem.stem,
                    "question": meaning
                    }


class Learner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    last_seen = db.Column(db.Date)
    learning_histories = db.relationship('LearningHistory',
                                         backref='learner',
                                         lazy='dynamic')

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


class LearningHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    combination_id = db.Column(db.Integer, db.ForeignKey('combination.id'))
    learner_id = db.Column(db.Integer, db.ForeignKey('learner.id'))
    direction = db.Column(db.Text)
    last_correct_date = db.Column(db.Date)
    ease = db.Column(db.Integer)

    @classmethod
    def get_question(cls, learner_id):
        question_type = random.choice([
                                       "different_prefix",
                                       # "different_stem"
                                       ])
        next_question = cls.query.filter_by(learner_id=learner_id).filter(
                            cls.last_correct_date != datetime.datetime.today()
                            ).first()
        if next_question:
            combination = Combination.query.filter_by(
                       next_question.first().combination_id).first()
            return combination.get_learning_info(question_type)
        else:
            combination = random.choice(Combination.query.all())
            return combination.get_learning_info(question_type)
