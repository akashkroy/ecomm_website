from flask import Flask
from flask import request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    firstname = StringField('First Name: ', validators=[DataRequired(),])
    lastname = StringField('Last Name: ', validators=[DataRequired()])
    email = StringField('Email: ', validators=[DataRequired(), Email('Enter a Valid Email')])
    password = PasswordField('Password: ', validators=[DataRequired(), Length(min=8, message='Password must be 8 Characters long')])
    confirm_password = PasswordField('Confirm Password: ', validators=[DataRequired(), EqualTo('password', message="Password doesn't match")])
    submit = SubmitField('Register')

class login_form(FlaskForm):
    email = StringField('Email: ', validators=[DataRequired(), Email(message='Enter a valid Email')])
    passwd = StringField('Password: ', validators=[DataRequired()])  
    submit = SubmitField('Log In')
