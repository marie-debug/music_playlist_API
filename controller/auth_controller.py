from flask import Blueprint, request,abort
from init import db, ma,bcrypt 
from models.user import User,UserSchema
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity
from datetime import timedelta
from models.playlist import Playlist,PlaylistSchema
from datetime import date



auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# get all the users from the database table if admin
@auth_bp.route("/users/", methods=["GET"])
@jwt_required()
def get_user():
    current_user_id= get_jwt_identity()
    statement= db.select(User).filter_by(id=current_user_id)
    user_scalar= db.session.scalar(statement)
    user= UserSchema().dump(user_scalar)
    print(user)
    if not user['is_admin']:
        abort(401)

    statement= db.select(User)
    user_scalar_list= db.session.scalars(statement)

    return UserSchema(many=True).dump(user_scalar_list)
    

#register new users
@auth_bp.route("/register/", methods=["POST"])
def auth_register():

    user_fields = request.json
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
@auth_bp.route('/login/', methods=['POST'])
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


