from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, validators


class NameForm(FlaskForm):
    name = TextAreaField(u'', [validators.Length(min=1)])

class AnswerForm(FlaskForm):
    combination_id = HiddenField(u'')
    question_type = HiddenField(u'')
    result = HiddenField(u'')
