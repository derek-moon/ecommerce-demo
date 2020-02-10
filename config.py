import os
from os import environ


basedir = os.path.dirname(os.path.abspath(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir,'app.db')}"
    SECRET_KEY = b'\xe0 \xea\xf788$\xbc\x04\x1e\xd6\xed \xda\xb6\x1a\xc9\x99\x06\xf0\x8b\x93\xf6\x90'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    