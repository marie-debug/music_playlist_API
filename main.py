from flask import Flask,request,abort
from flask_sqlalchemy import SQLAlchemy 
import os
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_jwt_extended import create_access_token,jwt_required,JWTManager



app = Flask(__name__)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


app.config["SQLALCHEMY_DATABASE_URI"]=os.environ['DATABASE_URL']
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')


db = SQLAlchemy(app)


class UserSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "firstname", "lastname", "email", "is_admin", "password")

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
            password=bcrypt.generate_password_hash('foobar231').decode("utf-8"),
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




@app.route("/users/", methods=["GET"])
def get_user():
    # get all the users from the database table

    statement= db.select(User)
    print (statement)
    user_list= db.session.scalars(statement)
    print(user_list)
    return UserSchema(many=True).dump(user_list)


#register new users
@app.route("/auth/register/", methods=["POST"])
def auth_register():

    user_fields = request.json
    print(user_fields)
    user = User()
    user.firstname = user_fields["firstname"]
    user.lastname = user_fields["lastname"]
    user.email = user_fields["email"]
    user.password = bcrypt.generate_password_hash(user_fields["password"]).decode("utf-8")
    db.session.add(user)
    db.session.commit()
    #Return the user to check the request was successful
    return UserSchema(exclude=['password']).dump(user), 201
 

# user login
@app.route('/login/', methods=['POST'])
def auth_login():
    # Find a user by email address
    stmt = db.select(User).filter_by(email=request.json['email'])
    user = db.session.scalar(stmt)
    # If user exists and password is correct
    if user and bcrypt.check_password_hash(user.password, request.json['password']):
        token = create_access_token(identity=str(user.id), expires_delta=timedelta(days=1))
        return {'email': user.email, 'token': token}

    else:
        return abort(401, description="Incorrect username and password")