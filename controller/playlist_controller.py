from flask import Blueprint, request
from init import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.playlist import Playlist, PlaylistSchema
from datetime import date
from controller.auth_controller import is_user_logged_in


playlist_bp = Blueprint('playlist', __name__, url_prefix='/playlist')


# get user playlists from the database table if logged in
@playlist_bp.route("/", methods=["GET"])
@jwt_required()
def get_playlist():

    user = is_user_logged_in()
    current_user_id = user.id

    statement = db.select(Playlist).filter_by(user_id=current_user_id)
    playlists = db.session.scalars(statement)
    return PlaylistSchema(many=True).dump(playlists)


# create playlist if logged in
@playlist_bp.route("/", methods=["POST"])
@jwt_required()
def create_playlist():

    current_user = get_jwt_identity()
    
    playlist_fields = request.json

    playlist = Playlist()

    playlist.creation_date= date.today()
    playlist.playlist_name = playlist_fields["playlist_name"]
    playlist.user_id = current_user
  
    db.session.add(playlist)
    db.session.commit()
    return {"name": playlist.playlist_name, "Date_Created": playlist.creation_date}

