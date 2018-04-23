from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length


class SubmitForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[Length(min=0, max=140)])
    submit = SubmitField('Send')

class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[Length(min=0, max=140)])
    submit = SubmitField('Send')
