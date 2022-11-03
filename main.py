from flask import Flask
from flask_sqlalchemy import SQLAlchemy 
import os
from flask_marshmallow import Marshmallow


app = Flask(__name__)
ma = Marshmallow(app)

app.config["SQLALCHEMY_DATABASE_URI"]=os.environ['DATABASE_URL']

db = SQLAlchemy(app)


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "firstname", "lastname", "email", "is_admin")

#single card schema, when one card needs to be retrieved
# user_schema = UserSchema()
#multiple card schema, when many cards need to be retrieved
user_schema = UserSchema(many=True)


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
            firstname = 'marion',
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




@app.route("/users", methods=["GET"])
def get_user():
    # get all the users from the database table

    statement= db.select(User)
    print (statement)
    user_list= db.session.scalars(statement)
    print(user_list)
    return UserSchema(many=True).dump(user_list)