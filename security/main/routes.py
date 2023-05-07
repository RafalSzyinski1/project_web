from flask import Blueprint, render_template, request, redirect
from flask_login import login_required

from security.models.models import KeyUsageHistory, Key, User

main = Blueprint('main', __name__)


@main.route("/about")
def about():
    return render_template("about.html", title="About")


@main.route("/history")
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    key_id = request.args.get('key', None, type=int)
    if key_id:
        key = Key.query.get_or_404(key_id)
        history = KeyUsageHistory.query.filter_by(key=key).order_by(
            KeyUsageHistory.date.desc()).paginate(page=page, per_page=10)
        return render_template("history.html", title=f"History of: {key.name}", history=history, key=key_id)
    user_id = request.args.get('user', None, type=int)
    if user_id:
        user = User.query.get_or_404(user_id)
        history = KeyUsageHistory.query.join(
            Key).filter_by(key_user=user).order_by(KeyUsageHistory.date.desc()).paginate(page=page, per_page=10)
        return render_template("history.html", title=f"History of: {user.name}", history=history, user=user_id)
    return redirect("/")
