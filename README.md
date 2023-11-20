## Childcare Enrollment Management System

`Deployed App`: [CCEEMS](https://childcare-d71b0285d615.herokuapp.com/)

* This is developed using Flask as the backend and HTML, CSS and JavaScript as the frontend.
* Python version `3.10.12` is required to build and run this application.
* If you plan to deploy this in heroku, please see Heroku's supported python runtimes and stacks [Heroku\'s Stacks & Python Support](https://devcenter.heroku.com/articles/python-support). Check the same for `AWS` as well.


### Install postgres in your local
- #### Installing PostgreSQL on macOS
    - ```brew install postgresql@16```
    - ```brew services start postgresql@16```
    - add the PostgreSQL binaries directory to your PATH by adding the following line to your shell profile file (such as ~/.zshrc if you're using Zsh):
      ```export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"```
    - ```source ~/.zshrc```
    - create a new database to setup local

- #### Installing PostgreSQL on Linux (Ubuntu)
    ```sh
    $ sudo sh -c 'echo "deb https://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
    $ wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
    $ sudo apt-get update
    $ sudo apt-get -y install postgresql
    ```
- #### Create a User in PostgreSQL for Local Setup
    Open a terminal window.
    Log in to PostgreSQL using:
    ```
    psql -U postgres
    ```
    
    Create a new user
    ```
    CREATE USER <your_username> WITH PASSWORD '<your_password>';
    ```
    
    Create a database
    ```
    CREATE DATABASE <your_database>;
    ```    
    
    Provide all privileges to your user for your database
    ```
    ALTER USER <your_username> WITH SUPERUSER;
    GRANT ALL PRIVILEGES ON DATABASE <your_database> TO <your_username>;
    ```
    
    Type `\q` to exit

##### Create your local connection string
Copy this string for use in the later steps for the local setup
```
DATABASE_URL=postgres://<your_username>:<your_password>@localhost:5432/<your_database>
Replace <your_username>, <your_password>, and <your_database> with your chosen values
```
### Steps to setup in local
1. Clone this repo using `git clone`
1. Install postgres and create the database and the user in your local machine following [install-postgres-in-your-local](#install-postgres-in-your-local)
1. Configure environment and configuration files:
   In the terminal type this.
   1. `export FLASK_ENV=development FLASK_SECRET_KEY=test DATABASE_URL={connectionString}`
   2. To permanently seed these values, add this command in your `bashrc` file.
      [See this for adding variables to .bashrc](https://askubuntu.com/questions/211716/add-environment-variable-to-bashrc-through-script)
1. Install the dependencies - `pip install -r requirements.txt`
1. Install pre-commit - `pre-commit install`
1. Run migrations - `flask --app main db upgrade`
1. Run seeds - `python seed.py`
1. Run the application using `flask --app main run`
1. Before you push your code, please format the code to follow the [pep8 standards](#code-formatting) and check your [code quality](#code-quality-check-pylint).

### Steps to Deploy (Heroku)
1. Clone this repo using `git clone`
4. Ensure the `Procfile` has the line `web: gunicorn main:app`. This means the file `main.py` will be used to run the flask application called `app`
5. Login to Heroku using `heroku login`. Verify your credentials in the browser. Use `heroku -i` to login without using the browser
6. Create a heroku app
   `heroku apps:create appName`
   If successful the command output will show the git repo url for this app. Make a note of it, it will be in the form `https://git.heroku.com/tanmai.git
8. Add the heroku git branch as a `remote` to your cloned repository. In the terminal type this `git remote add heroku [you heroku app's git url]`
10. Add the Postgresql addon for your app, using this link [Heroku Postgress Add-on](https://elements.heroku.com/addons/heroku-postgresql) (Must be logged in to Heroku)
11. Go to your app's resource page, go to [Dashboard](https://dashboard.heroku.com/apps).
    * Then click on your appname
    * Go to the resources tab.
    * Then click on Heroku Postgresql
    * On this page, go to settings and click on view credentials.
      Copy the database connection URI. It starts with `postgres://`
13. Using the terminal set the environment variables in Heroku for the flask application using this command `heroku config:set FLASK_APP=main FLASK_ENV=production FLASK_SECRET_KEY=test DATABASE_URL={your_connection_URI} --app yourHerokuAppName`
14. Push this repo to the heroku remote by doing `git push heroku main`. Wait for the deployment to finish.
15. Run the migrations in flask using this command `heroku run flask --app main db upgrade --app yourHerokuAppName`
16. Perform the seeding with this command `heroku run python seed.py --app yourHerokuAppName`
17. Type `heroku open` to open your app's homepage.

### Steps to run unit tests
1. Setup the project following the steps in [steps-to-setup-in-local](#steps-to-setup-in-local)
2. #### Setup the Test DB
   Create another database called `test`, and grant all privileges to your user for this database.
   Follow the same steps [Setup PSQL User](#create-a-user-in-postgreSQL-for-local-setup)
   Copy the connection string accordingly.
1. In a terminal, type this `export FLASK_ENV=test FLASK_SECRET_KEY=test DATABASE_URL_TEST={connectionURIForTestDB}`
   Seed the DATABASE_URL_TEST permanently into `.bashrc` if required. See this [How to set env variables in .bashrc](https://askubuntu.com/questions/211716/add-environment-variable-to-bashrc-through-script)
1. Run tests - `python -m unittest tests`
1. To run with coverage - `coverage run -m unittest discover -s tests`
1. Generate coverage report - `coverage report main.py config.py app/*.py`

### Steps to run behave tests
1. Setup the project following the steps in [steps-to-setup-in-local](#steps-to-setup-in-local)
1. In a terminal set these variables `export FLASK_ENV=test FLASK_SECRET_KEY=test DATABASE_URL_TEST={connectionURIForTestDB}`
   If you haven't seeded the `DATABASE_URL_TEST` in your `.bashrc` you must provide it here in the command
1. Run tests - `behave`
1. To run with coverage - `coverage run -m behave`

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
