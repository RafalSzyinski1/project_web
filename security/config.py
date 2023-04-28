import json
import pathlib

try:
    p = pathlib.Path(__file__).with_name("config.json")
    with p.open('r') as file:
        config = json.load(file)
except:
    # default
    config = {
        "SECRET_KEY": "5791628bb0b13ce0c676dfde280ba245",
        "SQLALCHEMY_DATABASE_URI": "sqlite:///site.db"
    }


class Config:
    SECRET_KEY = config["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = config["SQLALCHEMY_DATABASE_URI"]
