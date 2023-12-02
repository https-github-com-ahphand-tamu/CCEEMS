from flask import render_template, redirect
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
import logging
from app import create_app, db
from app.models import User, Case
from sqlalchemy import create_engine, text

from config import getUri

import os

app = create_app()
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "/user/login"
login_manager.init_app(app)

logging.basicConfig(level=logging.DEBUG)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', user=current_user)
    else:
        return redirect('/user/login')


if __name__ == '__main__':
    app.run(debug=True)
