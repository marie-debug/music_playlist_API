from flask import Blueprint, request, abort
from init import db, ma, bcrypt
from models.user import User, UserSchema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models.playlist import Playlist, PlaylistSchema
from datetime import date


playlist_bp = Blueprint('playlist', __name__, url_prefix='/playlist')


# get user playlist from the database table if logged in
@playlist_bp.route("/", methods=["GET"])
@jwt_required()
def get_playlist():
    current_user_id = get_jwt_identity()
    statement = db.select(User).filter_by(id=current_user_id)
    user_scalar = db.session.scalar(statement)
    user = UserSchema().dump(user_scalar)
    print(user)
    if not user:
        abort(401)

    statement = db.select(Playlist)
    playlist = db.session.scalars(statement)
    return PlaylistSchema(many=True).dump(playlist)


# create playlist if logged in
@playlist_bp.route("/", methods=["POST"])
@jwt_required()
def create_playlist():
    current_user_id = get_jwt_identity()

    statement = db.select(User).filter_by(id=current_user_id)
    user_scalar = db.session.scalar(statement)
    user = UserSchema().dump(user_scalar)
    if not user:
        abort(401)

    data = PlaylistSchema().load(request.json)

    playlist = Playlist(

        playlist_name=data['playlist_name'],
        creation_date=date.today()

    )

    db.session.add(playlist)
    db.session.commit()

    return PlaylistSchema().dump(playlist)
