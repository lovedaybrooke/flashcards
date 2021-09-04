from flask import Flask
from flask import render_template, redirect, request

from app import app, db
from app.forms import NameForm
from app.models import *


@app.route('/', methods=['GET', 'POST'])
def home():
    form = NameForm()
    if request.method == "POST" and form.validate_on_submit():
        learner = Learner.create_or_find(form.name.data)
        return render_template('home.html', learner=learner)
    else:
        return render_template('home.html', form=form)
