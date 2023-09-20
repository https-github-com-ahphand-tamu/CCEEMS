from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import config
from flask_migrate import Migrate

CCEMS = Flask(__name__)
CCEMS.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URI
db = SQLAlchemy(CCEMS)
migrate = Migrate(CCEMS, db)

@CCEMS.route('/')
def landingRoute():
   return render_template('index.html')

if __name__ == '__main__':
    CCEMS.run()
