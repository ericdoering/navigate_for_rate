from setuptools import Require
from wtforms import SelectField, TextAreaField, StringField, IntegerField, FloatField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length, NumberRange, Optional
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    """Allow user to sign in"""
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=30)])


class RegisterForm(FlaskForm):
    """Validates creation of new user"""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=30)])
    first_name = StringField("First Name", validators=[InputRequired(), Length(max=20)])
    last_name = StringField("Last Name", validators=[InputRequired(), Length(max=30)])
    company = StringField("Company", validators=[InputRequired()])
    state = StringField("State", validators=[InputRequired()])


class RouteForm(FlaskForm):
    """Validates user creating new driving route"""

    type = ("Business", "Medical/Moving", "Charitable")

    start_point = TextAreaField("Start Point", validators=[InputRequired()])
    end_point = TextAreaField("End Point", validators=[InputRequired()])
    travel_type = SelectField("Travel Type", validators=[InputRequired()], choices=[(choice, choice) for choice in type])
    comments = TextAreaField("Comments")

class DeleteForm(FlaskForm):
    """Clears a driving route"""