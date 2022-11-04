from flask import Blueprint, request,abort
from init import db, ma,bcrypt 
from models.user import User,UserSchema
from flask_jwt_extended import create_access_token,jwt_required,JWTManager
from datetime import timedelta




users_bp = Blueprint('users', __name__, url_prefix='/users')



@users_bp.route("/", methods=["GET"])
def get_user():
    # get all the users from the database table

    statement= db.select(User)
    print (statement)
    user_list= db.session.scalars(statement)
    return UserSchema(many=True).dump(user_list)


#register new users
@users_bp.route("/auth/register/", methods=["POST"])
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
@users_bp.route('/login/', methods=['POST'])
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