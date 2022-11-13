from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.playlist import Playlist, PlaylistSchema
from models.song import Song
from datetime import date
from controller.auth_controller import is_user_logged_in

playlist_bp = Blueprint('playlist', __name__, url_prefix='/playlist')


# get user playlists from the database table if logged in
@playlist_bp.route("/", methods=["GET"])
@jwt_required()
def get_playlists():
    user = is_user_logged_in()
    current_user_id = user.id
# selects playlist from db and filters by the user id
    statement = db.select(Playlist).filter_by(user_id=current_user_id)
    playlists = db.session.scalars(statement)
    return PlaylistSchema(many=True).dump(playlists)



# get user playlist from the database table if logged in
@playlist_bp.route("/<int:playlist_id>/'", methods=["GET"])
@jwt_required()
def get_playlist(playlist_id):
        user = is_user_logged_in()
        if user:
    # selects playlist from db and filters by the user id
            statement = db.select(Playlist).filter_by(id = playlist_id)
            playlist = db.session.scalar(statement)
            return PlaylistSchema().dump(playlist)

        return {'error': f'playlist not found with id {playlist_id}'}, 500



# create playlist if logged in
@playlist_bp.route("/", methods=["POST"])
@jwt_required()
def create_playlist():
    current_user = get_jwt_identity()
    playlist_fields = request.json

    playlist = Playlist()
    playlist.creation_date = date.today()
    playlist.name = playlist_fields["playlist_name"]
    playlist.user_id = current_user
    # adds plalist fields into the db
    db.session.add(playlist)
    db.session.commit()
    return {"name": playlist.playlist_name, "Date_Created": playlist.creation_date, "playlist_name": playlist.id}


#creates a new song in a given playlist
@playlist_bp.route("/<int:playlist_id>/songs/", methods=["POST"])
@jwt_required()
def create_song(playlist_id):
        is_user_logged_in()
        # selects playlist from db based on playlist id
        stmt = db.select(Playlist).filter_by(id=playlist_id)
        playlist = db.session.scalar(stmt)
       
        song_fields = request.json

        if playlist:
            song = Song()
            song.genre = song_fields["genre"]
            song.name = song_fields["name"]
            song.playlist_id = playlist.id

            # adds songs fields into the db
            db.session.add(song)
            db.session.commit()
            return {"name": song.name, "genre": song.genre, "playlist": playlist.playlist_name}
        return {'error': f'playlist not found with id {playlist_id}'}, 500


# deletes a song from the database
@playlist_bp.route("/<int:playlist_id>/songs/<int:song_id>/", methods=['DELETE'])
@jwt_required()
def delete_song(playlist_id,song_id):
        is_user_logged_in()
        # select playlist from database
        stmt = db.select(Playlist).filter_by(id=playlist_id)
        playlist = db.session.scalar(stmt)

        # select song from database 
        stmt = db.select(Song).filter_by(id=song_id)
        song = db.session.scalar(stmt)

        if song and playlist:
            db.session.delete(song)
            db.session.commit()
            return {'message': f"Song '{song.name}' deleted successfully"}
        else:
            return {'error': f'Song not found with id {id}'}, 404


@playlist_bp.route('/<int:playlist_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_playlist(playlist_id):

    stmt = db.select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    if playlist:
        playlist.name = request.json.get('name') or playlist.name
        db.session.commit()      
        return PlaylistSchema().dump(playlist)
    else:
        return {'error': f'playlist not found with id {playlist_id}'}, 404


@playlist_bp.route("/<int:id>/", methods=['DELETE'])
@jwt_required()
def delete_playlist(id):
    user = is_user_logged_in()
    current_user_id = user.id
    # gets playlist from db filtered by the user name and the playlist id
    stmt = db.select(Playlist).filter_by(user_id=current_user_id, id=id)
    playlist = db.session.scalar(stmt)
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        return {'message': f"Playlist '{playlist.playlist_name}' deleted successfully"}
    else:
        return {'error': f'playlist not found with id {id}'}, 404



