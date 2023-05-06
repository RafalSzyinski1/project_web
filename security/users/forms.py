from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, EqualTo
from flask_login import current_user

from security.models.models import User


class UpdateAccountForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    surname = StringField('Surname', validators=[
                          DataRequired(), Length(min=2, max=20)])

    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email is taken. Please choose a different one.')


class UpdateAccountPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Update')
