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

    def append_hint(self):
        if self.hint:
            return self.meaning + " " + self.hint
        else:
            return self.meaning


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
        wrong_answer = self.get_wrong_answer(question_type)
        if question_type == "different_meaning":
            right_answer = meaning.append_hint()
            question = {"question": prefix.prefix+stem.stem }
        else:
            right_answer = prefix.prefix+stem.stem
            question = {
                        "question": meaning.meaning,
                        "hint": meaning.hint
                       }
        answers = [
                    {"text": right_answer,
                     "correct": "right"},
                    {"text": wrong_answer,
                     "correct": "wrong"}
                  ]
        random.shuffle(answers)
        return {"question_type": question_type,
                "combination_id": self.id,
                "answers": answers,
                "question": question}

    def get_wrong_meaning(self):
        right_meaning_ids = [combi.meaning_id for combi in Combination.query
                             .filter_by(prefix_id=self.prefix_id)
                             .filter_by(stem_id=self.stem_id).all()]
        wrong_meanings = [m.append_hint() for m in VerbMeaning.query.all()
                          if m.id not in right_meaning_ids]
        return random.choice(wrong_meanings)

    def get_wrong_stem(self):
        right_prefix = VerbPrefix.query.filter_by(
                           id=self.prefix_id).first().prefix
        alternate_stem_ids = [combi.stem_id for combi in Combination.query
                              .filter_by(prefix_id=self.prefix_id)
                              .filter(Combination.stem_id != self.stem_id)
                              .filter(Combination.meaning_id != self.meaning_id)
                              .all()]
        wrong_stems = [s.stem for s in VerbStem.query.all()
                       if s.id in alternate_stem_ids]
        return right_prefix+random.choice(wrong_stems)

    def get_wrong_prefix(self):
        right_stem = VerbStem.query.filter_by(
                         id=self.stem_id).first().stem
        alternate_prefix_ids = [combi.prefix_id for combi in Combination.query
                                .filter_by(stem_id=self.stem_id)
                                .filter(Combination.prefix_id != self.prefix_id)
                                .filter(Combination.meaning_id != self.meaning_id)
                                .all()]
        wrong_prefixes = [p.prefix for p in VerbPrefix.query.all()
                          if p.id in alternate_prefix_ids]
        return random.choice(wrong_prefixes)+right_stem

    def get_wrong_answer(self, question_type):
        if question_type == "different_prefix":
            return self.get_wrong_prefix()
        elif question_type == "different_stem":
            return self.get_wrong_stem()
        elif question_type == "different_meaning":
            return self.get_wrong_meaning()


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
            LearningHistory.generate_blank_history(new_learner.id)
            return new_learner


class LearningHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    combination_id = db.Column(db.Integer, db.ForeignKey('combination.id'))
    learner_id = db.Column(db.Integer, db.ForeignKey('learner.id'))
    direction = db.Column(db.Text)
    last_correct_date = db.Column(db.Date)
    last_asked_date = db.Column(db.Date)
    ease = db.Column(db.Integer)

    @classmethod
    def convert_question_type(cls, question_type):
        if question_type == "different_meaning":
            return "ger_to_eng"
        else:
            return "eng_to_ger"

    @classmethod
    def generate_blank_history(cls, learner_id):
        combinations = [c.id for c in Combination.query.all()]
        directions = ["ger_to_eng", "eng_to_ger"]
        for c in combinations:
            for d in directions:
                history = cls.query.filter_by(learner_id=learner_id,
                                              combination_id=c,
                                              direction=d).first()
                if not history:
                    history = cls(learner_id=learner_id,
                                  combination_id=c,
                                  direction=d,
                                  ease=0)
                    db.session.add(history)
                    db.session.commit()

    @classmethod
    def get_question(cls, learner_id):
        question_type = random.choice([
                                       "different_prefix"
                                       # "different_stem",
                                       # "different_meaning"
                                       ])

        today = datetime.datetime.today().date()
        new = cls.query.filter_by(learner_id=learner_id
                      ).filter(cls.last_asked_date == None
                      ).all()
        never_right = cls.query.filter_by(learner_id=learner_id
                              ).filter(cls.last_correct_date == None
                              ).order_by(cls.ease.asc()
                              ).all()
        not_right_today = cls.query.filter_by(learner_id=learner_id
                                    ).filter(cls.last_correct_date != today
                                    ).order_by(cls.ease.asc()
                                    ).all()
        everything_hard = cls.query.filter_by(learner_id=learner_id
                                    ).filter(cls.ease < 1
                                    ).order_by(cls.ease.asc()
                                    ).all()
        everything_else = cls.query.filter_by(learner_id=learner_id
                                    ).all()

        if new:
            next_question = random.choice(new)
        elif never_right:
            next_question = never_right[0]
        elif not_right_today:
            next_question = not_right_today[0]
        elif everything_hard:
            next_question = everything_hard[0]
        else:
            next_question = random.choice(everything_else)

        combination = Combination.query.filter_by(
                              id=next_question.combination_id).first()
        return combination.get_learning_info(question_type)

    @classmethod
    def update(cls, learner_id, combination_id, question_type, correct):
        history = cls.query.filter_by(learner_id=learner_id,
                                      combination_id=int(combination_id),
                                      direction=cls.convert_question_type(question_type)
                                      ).first()
        history.last_asked_date = datetime.datetime.today()
        if correct == "right":
            history.last_correct_date = datetime.datetime.today()
            history.ease += 1
        else:
            history.ease -= 1
        db.session.add(history)
        db.session.commit()
