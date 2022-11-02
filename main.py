from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import os

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ['DATABASE_URL']

db = SQLAlchemy(app)




class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)



@app.cli.command('seed')
def seed_db():
    users = [
        User(
            firstname= 'marion',
            lastname = 'akinyi',
            email='admin@spam.com',
            password='foobar231',
            is_admin=True
        )
    ]

    db.session.add_all(users)
    db.session.commit()

# create app's cli command named create, then run it in the terminal as "flask create", 
# it will invoke create_db function
@app.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 