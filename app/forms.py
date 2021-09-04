from flask_wtf import FlaskForm
from wtforms import TextAreaField, validators


class NameForm(FlaskForm):
    name = TextAreaField(u'', [validators.Length(min=1)])
