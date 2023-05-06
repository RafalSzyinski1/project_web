from flask import (Blueprint, render_template,
                   url_for, flash, redirect, request)
from flask_login import (login_user, current_user, logout_user, login_required)

from security import db, bcrypt
from security.login.forms import LoginForm
from security.models.models import User

login = Blueprint('login', __name__)


@login.route("/", methods=['GET', 'POST'])
@login.route("/home", methods=['GET', 'POST'])
@login.route("/login", methods=['GET', 'POST'])
def login_to():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            next_page = request.args.get('next')
            login_user(user)
            return redirect(next_page) if next_page else redirect(url_for('users.account'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@login.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login.login_to'))
