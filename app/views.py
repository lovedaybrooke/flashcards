from flask import Flask
from flask import render_template, redirect, request

from app import app, db
from app.forms import *
from app.models import *


@app.route('/', methods=['GET', 'POST'])
def home():
    form = NameForm()
    if request.method == "POST" and form.validate_on_submit():
        learner = Learner.create_or_find(form.name.data)
        return redirect('learn/{0}'.format(learner.id))
    else:
        return render_template('home.html', form=form)


@app.route('/learn/<learner_id>', methods=['GET', 'POST'])
def learn(learner_id):
    form = AnswerForm()
    if request.method == "POST":
        LearningHistory.update(learner_id, form.combination_id.data,
                               form.question_type.data, form.result.data)
    next_question = LearningHistory.get_question(learner_id)
    return render_template('learn.html',
                           learner_id=learner_id,
                           combination=int(next_question["combination_id"]),
                           answers=next_question["answers"],
                           question=next_question["question"],
                           question_type=next_question["question_type"],
                           form=form)
