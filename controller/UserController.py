from flask import Blueprint, request


# users_bp = Blueprint('users', __name__, url_prefix='/users')



# @users_bp.route('/')
# # @jwt_required()
# def get_all_users():
#     # return 'all_cards route'
#     # if not authorize():
#     #     return {'error': 'You must be an admin'}, 401

#     stmt = db.select(User)
#     users = db.session.scalars(stmt)
#     return UserSchema(many=True).dump(users)