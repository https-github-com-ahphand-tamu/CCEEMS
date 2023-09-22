from flask import Flask, render_template
from users import get_all_users

CCEEMS = Flask(__name__)

@CCEEMS.route('/')
def landingRoute():
   return render_template('index.html')

@CCEEMS.route('/users')
def users():
    users_data = get_all_users()
    return render_template('users.html', users=users_data)

if __name__ == '__main__':
    CCEEMS.run()