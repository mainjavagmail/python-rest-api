# Python RESTful API
Python API using micro framework Flask.

### Project details
* Python 3.7
* Flask
* SQLAlchemy
* PostgreSQL

### How to use
After clone this project from github, you will use the requirements.txt to manage your virtual environment.
Create an environment variable called SQLALCHEMY_DATABASE_URI with database connection (eg: postgresql://postgres:a@localhost/banco) or change it on app.py file.

```
git clone https://github.com/vitoralves/python-rest-api
cd python-rest-api
pip install -r requirements.txt
python app.py
endpoints access on localhost:5000/
```