from flask import (Blueprint, render_template,
                   url_for, flash, redirect, request)
from flask_login import (login_user, current_user, logout_user, login_required)

from security import db, bcrypt
from security.users.forms import UpdateAccountForm
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
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('update_account.html', title='Update Account',
                           image_file=image_file, form=form)
