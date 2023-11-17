## Childcare Enrollment Management System

`Deployed App`: [CCEEMS](https://childcare-d71b0285d615.herokuapp.com/)

* This is developed using Flask as the backend and HTML, CSS and JavaScript as the frontend.
* Python version `3.10.12` is required to build and run this application.
* If you plan to deploy this in heroku, please see Heroku's supported python runtimes and stacks [Heroku\'s Stacks & Python Support](https://devcenter.heroku.com/articles/python-support). Check the same for `AWS` as well.


### Install postgres in your local
- Installing PostgreSQL on macOS
    - ```brew install postgresql@16```
    - ```brew services start postgresql@16```
    - add the PostgreSQL binaries directory to your PATH by adding the following line to your shell profile file (such as ~/.zshrc if you're using Zsh):
      ```export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"```
    - ```source ~/.zshrc```

- Installing PostgreSQL on Linux (Ubuntu)
    ```sh
    $ sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    $ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    $ sudo apt-get update
    $ sudo apt-get -y install postgresql
    ```

### Steps to setup in local
1. Clone this repo using `git clone`
1. Install postgres in your local machine following [install-postgres-in-your-local](#install-postgres-in-your-local)
1. Configure environment and configuration files:
   1. Set database url - `export DATABASE_URL="postgresql://[username]:[password]@localhost:5432/[dbname]"`
   1. Copy file and change values in .env - `cp .env.example .env`
   1. Export env values - `export $(xargs <.env)`
1. Install the dependencies - `pip install -r requirements.txt`
1. Install pre-commit - `pre-commit install`
1. Run migrations - `flask --app main db upgrade`
1. Run seeds - `python seed.py`
1. Run the application using `flask --app main run` or `gunicorn main:app`
1. Before you push your code, please format the code to follow the [pep8 standards](#code-formatting) and check your [code quality](#code-quality-check-pylint).

### Steps to Deploy (Heroku)
1. Clone this repo using `git clone`
1. Install the dependencies using `pip install -r requirements.txt`
1. Run the application using `flask --app main run` or `gunicorn main:app`
    This will provide a link to the application. Open it and verify the `index.html` site is rendered and the heading says `Childcare Enrollment Management System`
1. Ensure the `Procfile` has the line `web: gunicorn main:app`. This means the file `main.py` will be used to run the flask application called `app`
1. Login to Heroku using `heroku login`. Verify your credentials in the browser. Use `heroku -i` to login without using the browser
1. Add the heroku git branch as a `remote` to your cloned repository. The command is `git remote add heroku [you heroku app's git url]`
2. Push this repo to the heroku remote by doing `git push heroku main`. Wait for the deployment to finish.
3. Set the environment variables in Heroku for the flask application using this command `heroku config:set FLASK_APP=main FLASK_ENV=production FLASK_SECRET_KEY=test DATABASE_URL={your_connection_string}`
4. Run the migrations in flask using this command `heroku run flask --app main db upgrade --app yourHerokuAppName`
5. Perform the seeding with this command `heroku run python seed.py --app yourHerokuAppName`.
6. Type `heroku open` to open your app's homepage.

### Steps to run unit tests
1. Setup the project following the steps in [steps-to-setup-in-local](#steps-to-setup-in-local)
1. In `.env` file, set `FLASK_ENV=test`
1. Run tests - `python -m unittest tests`
1. Run with coverage - `coverage run -m unittest discover -s tests`
1. Generate coverage report - `coverage report -m --omit="tests/*"`

### Steps to run behave tests
1. Setup the project following the steps in [steps-to-setup-in-local](#steps-to-setup-in-local)
1. In `.env` file, set `FLASK_ENV=test`
1. Run tests - `behave`
1. Get coverage - `coverage run -m behave`


### Code formatting
To automatically format the code to follow the pep8 style guide, run the following command:
```
autopep8 --in-place --recursive app main.py seed.py
```

### Code Quality Check (Pylint)
To check the code quality using pylint, run the following command:
```
pylint app
```
