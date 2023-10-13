from flask import render_template
from flask_login import LoginManager
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
def login():
    return render_template('Login.html')


@app.route('/index')
def home():
    return render_template('index.html')

@app.route('/users/setpassword')
def setPassword():
    return render_template('password.html')

if __name__ == '__main__':
    app.run(debug=True)
