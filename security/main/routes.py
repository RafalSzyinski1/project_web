from flask import Blueprint

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    return "<h1>HELLO</h1>"


def about():
    pass
