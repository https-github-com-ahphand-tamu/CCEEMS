from flask import Flask, render_template
from users import get_all_users

CCEMS = Flask(__name__)

@CCEMS.route('/')
def landingRoute():
   return render_template('index.html')

@CCEMS.route('/users')
def users():
    users_data = get_all_users()
    return render_template('users.html', users=users_data)

if __name__ == '__main__':
    CCEMS.run()