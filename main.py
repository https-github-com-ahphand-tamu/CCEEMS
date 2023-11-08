from flask import render_template, redirect
from flask_login import LoginManager, current_user
from flask_migrate import Migrate

from app import create_app, db
from app.models import User

app = create_app()
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = "/user/login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home-page.html')
    else:
        return redirect('/user/login')


if __name__ == '__main__':
    app.run(debug=True)
