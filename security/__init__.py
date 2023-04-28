from flask import Flask
from security.config import Config


def create_app(config_class=Config):
    print(config_class.SECRET_KEY)
    print(config_class.SQLALCHEMY_DATABASE_URI)
