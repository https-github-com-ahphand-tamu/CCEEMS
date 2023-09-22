from flask import Flask, render_template

CCEEMS = Flask(__name__)

@CCEEMS.route('/')
def landingRoute():
   return render_template('index.html')

if __name__ == '__main__':
    CCEEMS.run()
