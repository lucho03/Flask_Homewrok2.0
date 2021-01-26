from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class Registration(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign up')

class Login(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min = 2, max = 30)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')