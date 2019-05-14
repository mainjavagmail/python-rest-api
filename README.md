# Python RESTful API
Python API using micro framework Flask.

### Project details
* Python 3.7
* Flask
* SQLAlchemy
* PostgreSQL
* Flask-JWT

### How to use
After clone this project from github, you will use the requirements.txt to manage your virtual environment.

Create an environment variable called SQLALCHEMY_DATABASE_URI with database connection (eg: postgresql://postgres:a@localhost/banco) and JWT_SECRET_KEY with a string value, this is used to create tokens. You can change these values on app.py file.

```
git clone https://github.com/vitoralves/python-rest-api
cd python-rest-api
pip install -r requirements.txt
python app.py
endpoints access on localhost:5000/
```

Use route /cadastro to create a new user and route /login to get a token.
