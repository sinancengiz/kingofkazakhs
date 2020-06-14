from flask_wtf import Form
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)
from models import Player

def name_exists(form, field):
    if Player.select().where(Player.player_name == field.data).exists():
        raise ValidationError('Player with that name already exists.')

def email_exists(form, field):
    if Player.select().where(Player.email == field.data).exists():
        raise ValidationError('Player with that email already exists.')

class RegisterForm(Form):
    player_name = StringField(
        'Player_Name',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message=("Player_name should be one word, letters, "
                         "numbers, and underscores only.")
            ),
            name_exists
        ])
    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])
    password2 = PasswordField(
        'Confirm Password',
        validators=[DataRequired()]
    )

class LoginForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])



