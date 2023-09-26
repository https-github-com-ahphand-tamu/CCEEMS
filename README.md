## Childcare Enrollment Management System

`Deployed App`: [CCEEMS](https://childcare-d71b0285d615.herokuapp.com/)

* This is developed using Flask as the backend and HTML, CSS and JavaScript as the frontend. 
* Python version `3.10.12` is required to build and run this application. 
* If you plan to deploy this in heroku, please see Heroku's suppoted python runtimes and stacks [Heroku\'s Stacks & Python Support](https://devcenter.heroku.com/articles/python-support). Check the same for `AWS` as well.


### Steps to setup in local
1. Clone this repo using `git clone`
1. Install postgres in your local
1. Configure environment and configuration files:
   1. Copy file and change values in config.py - `cp config.example.py config.py`
   2. Copy file and change values in .env - `cp .env.example .env`
1. Install the dependencies - `pip install -r requirements.txt`
1. Run migrations - `flask --app main db upgrade`
1. Run seeds - `python seed.py`
1. Run the application using `flask --app main run` or `gunicorn main:app`


### Steps to Deploy (Heroku)
1. Clone this repo using `git clone`
1. Install the dependencies using `pip install -r requirements.txt`
1. Run the application using `flask --app main run` or `gunicorn main:app`
    This will provide a link to the application. Open it and verify the `index.html` site is rendered and the heading says `Childcare Enrollment Management System`
1. Ensure the `Procfile` has the line `web: gunicorn main:app`. This means the file `main.py` will be used to run the flask application called `app`
1. Login to Heroku using `heroku login`. Verify your credentials in the browswer. Use `heroku -i` to login without using the browser
1. Add the heroku git branch as a `remote` to your cloned repository. Command is `git remote add heroku [you heroku app's git url]`
1. Push this repo the heroku remote by doing `git push heroku main`. Wait for the deployment to finish and verify the app is running on heroku
