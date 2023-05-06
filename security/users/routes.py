from flask import (Blueprint, render_template,
                   url_for, flash, redirect, request)
from flask_login import (login_user, current_user, logout_user, login_required)

from security import db, bcrypt
from security.users.forms import UpdateAccountForm, UpdateAccountPasswordForm
from security.users.utils import save_picture

users = Blueprint('users', __name__)


@users.route("/account")
@login_required
def account():
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file)


@users.route("/account/update", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.name = form.name.data
        current_user.surname = form.surname.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.surname.data = current_user.surname
        form.email.data = current_user.email
    return render_template('update_account.html', title='Update Account', form=form)


@users.route("/account/update_password", methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdateAccountPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        if not bcrypt.check_password_hash(current_user.password, form.password.data):
            current_user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('users.account'))
        else:
            flash('New password cannot be the same as old password', 'danger')
    return render_template('update_password.html', title='Update Account', form=form)
