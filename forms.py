from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from database import User

class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    image = FileField('Picture', validators=[FileAllowed(['png', 'jpg'])])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This name is already exists! Choose different one')

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Post(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')