from flask import (Blueprint, render_template,
                   url_for, flash, redirect, request, abort)
from flask_login import (login_user, current_user, logout_user, login_required)

from security import db, bcrypt
from security.users.forms import UpdateAccountForm, UpdateAccountPasswordForm, AdminUpdateAccountForm
from security.users.utils import save_picture
from security.models.models import Key, User, Lock, KeyLocks

users = Blueprint('users', __name__)


@users.route("/account")
@login_required
def account():
    keys = Key.query.filter_by(
        key_user=current_user).order_by(Key.name.asc()).all()
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, keys=keys)


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
        if not bcrypt.check_password_hash(current_user.password, form.old_password.data):
            flash('Old password is wrong', 'danger')
        else:
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


@users.route("/users")
@login_required
def update_users():
    if not current_user.is_admin:
        abort(403)
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(
        User.surname.asc()).paginate(page=page, per_page=5)
    return render_template("users.html", title="Update Users", users=users)


@users.route("/users/<int:user_id>/edit_account", methods=["GET", "POST"])
@login_required
def edit_users_account(user_id):
    if not current_user.is_admin:
        abort(403)
    form = AdminUpdateAccountForm()
    user = User.query.get_or_404(user_id)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            user.image_file = picture_file
        user.name = form.name.data
        user.surname = form.surname.data
        user.is_admin = form.admin.data
        db.session.commit()
        flash(f'{user.name} account has been updated!', 'success')
        return redirect(url_for('users.update_users'))
    elif request.method == 'GET':
        form.name.data = user.name
        form.surname.data = user.surname
        form.admin.data = user.is_admin
    return render_template('admin_edit_user.html', title='Edit user', form=form)


@users.route("/users/<int:user_id>/restart_password")
@login_required
def restart_password(user_id):
    if not current_user.is_admin:
        abort(403)
    user = User.query.get_or_404(user_id)
    user.admin_restart_password()
    flash(
        f'Password was restarted for {user.name}. Password contain first letter of name concat with surname', 'info')
    return redirect(url_for('users.account'))


@users.route("/keys")
@login_required
def update_keys():
    if not current_user.is_admin:
        abort(403)
    page = request.args.get('page', 1, type=int)
    keys = Key.query.order_by(
        Key.name.asc()).paginate(page=page, per_page=5)
    return render_template("keys.html", title="Update Keys", keys=keys)


@users.route("/keys/show_locks_for_key/<int:key_id>")
@login_required
def key_show_locks(key_id):
    if not current_user.is_admin:
        abort(403)
    Key.query.get_or_404(key_id)
    page = request.args.get('page', 1, type=int)
    locks = Lock.query.paginate(page=page, per_page=10)
    key_locks = Lock.query.join(KeyLocks).filter(
        KeyLocks.key_id == key_id).all()
    return render_template('locks_for_key.html', locks=locks, key_locks=key_locks, key_id=key_id, page=page)


@users.route("/keys/add_key_to_lock/<int:key_id>")
@login_required
def key_add_lock(key_id):
    if not current_user.is_admin:
        abort(403)
    Key.query.get_or_404(key_id)

    lock_id = request.args.get('lock_id', None, type=int)
    page = request.args.get('page', 1, type=int)

    if key_id and lock_id:
        key_lock = KeyLocks(key_id=key_id, lock_id=lock_id)
        db.session.add(key_lock)
        db.session.commit()
        flash('Lock has been added', 'info')
    else:
        flash('Something wrong. Cannot add this lock to key', 'danger')
    return redirect(url_for('users.key_show_locks', key_id=key_id, page=page))


@users.route("/keys/remove_key_to_lock/<int:key_id>")
@login_required
def key_remove_lock(key_id):
    if not current_user.is_admin:
        abort(403)
    Key.query.get_or_404(key_id)

    lock_id = request.args.get('lock_id', None, type=int)
    page = request.args.get('page', 1, type=int)
    if key_id and lock_id:
        key_lock = KeyLocks.query.filter_by(
            key_id=key_id).filter_by(lock_id=lock_id).first_or_404()
        print(key_lock)
        db.session.delete(key_lock)
        db.session.commit()
        flash('Lock has been removed', 'info')
    else:
        flash('Something wrong. Cannot add this lock to key', 'danger')
        return redirect("/")
    return redirect(url_for('users.key_show_locks', key_id=key_id, page=page))


@users.route("/locks")
@login_required
def update_locks():
    if not current_user.is_admin:
        abort(403)
    page = request.args.get('page', 1, type=int)
    locks = Lock.query.order_by(
        Lock.name.asc()).paginate(page=page, per_page=5)
    return render_template("locks.html", title="Update Locks", locks=locks)
