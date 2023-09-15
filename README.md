## Childcare Enrollment Management System

`Deployed App`: [https://childcare-d71b0285d615.herokuapp.com/](CCEEMS)

* This is developed using Flask as the backend and HTML, CSS and JavaScript as the frontend. 
* Python version `3.10.12` is required to build and run this application. 
* If you plan to deploy this in heroku, please see Heroku's suppoted python runtimes and stacks [https://devcenter.heroku.com/articles/python-support](Heroku's Stacks & Python Support). Check the same for `AWS` as well.

### Steps to Deploy (Heroku)
1. Clone this repo using `git clone`
2. Install the dependencies using `pip install -r requirements.txt`
3. Login to Heroku using `heroku login`. Verify your credentials in the browswer. Use `heroku -i` to login without using the browser
4. Run the application using `flask --app main run` or `gunicorn main:CCEEMS`

    This will provide a link to the application. Open it and verify the `index.html` site is rendered and the heading says `Childcare Enrollment Management System`

5. Ensure the `Procfile` has the line `web: gunicorn main:CCEEMS`. This means the file `main.py` will be used to run the flask application called `CCEEMS`
6. Add the heroku git branch as a `remote` to your cloned repository. Command is `git remote add heroku [you heroku app's git url]`
7. Push this repo the heroku remote by doing `git push heroku main`. Wait for the deployment to finish and verify the app is running on heroku