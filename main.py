from app import create_app, db
from flask import render_template
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)


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
