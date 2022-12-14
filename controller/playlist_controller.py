from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from init import db
from models.playlist import Playlist, PlaylistSchema
from models.song import Song, SongSchema
from datetime import date
from controller.auth_controller import is_user_logged_in

playlist_bp = Blueprint('playlist', __name__, url_prefix='/playlists')


# get user playlists from the database table if logged in
@playlist_bp.route("/", methods=["GET"])
@jwt_required()
def get_playlists():
    user = is_user_logged_in()
    current_user_id = user.id
# selects playlist from db and filters by the user id
    statement = db.select(Playlist).filter_by(user_id=current_user_id)
    playlists = db.session.scalars(statement)
    result = PlaylistSchema(many=True).dump(playlists)
    if len(result) >= 1:
        return result
    return {'error': f'please create playlist for {user.firstname}'}, 404


# get user playlist from the database table if logged in
@playlist_bp.route("/<int:playlist_id>/", methods=["GET"])
@jwt_required()
def get_playlist(playlist_id):
    user = is_user_logged_in()
    current_user_id = user.id
    # selects playlist from db and filters by the user id and playlist id
    statement = db.select(Playlist).filter_by(
        user_id=current_user_id, id=playlist_id)
    playlist = db.session.scalar(statement)
    result = PlaylistSchema().dump(playlist)
    if result:
        return result

    return {'error': f'playlist not found with id {playlist_id}'}, 404


# create playlist if logged in
@playlist_bp.route("/", methods=["POST"])
@jwt_required()
def create_playlist():

    current_user = get_jwt_identity()

    data = PlaylistSchema().load(request.json)
    playlist = Playlist(
        name=data['name'],
        creation_date=date.today(),
        user_id=current_user

    )
    # adds playlist fields into the db
    db.session.add(playlist)
    db.session.commit()
    return PlaylistSchema().dump(playlist), 201


# creates a new song in a given playlist
@playlist_bp.route("/<int:playlist_id>/songs/", methods=["POST"])
@jwt_required()
def create_song(playlist_id):
    is_user_logged_in()
    # selects playlist from db based on playlist id
    stmt = db.select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)

    if playlist:
        data = SongSchema().load(request.json)
        song = Song(
            name=data['name'],
            genre=data['genre'],
            artist=data['artist'],
            playlist_id=playlist_id

        )
        # adds songs fields into the db
        db.session.add(song)
        db.session.commit()
        return SongSchema().dump(song), 201
    return {'error': f'playlist not found with id {playlist_id}'}, 500


# deletes a song from the database
@playlist_bp.route("/<int:playlist_id>/songs/<int:song_id>/", methods=['DELETE'])
@jwt_required()
def delete_song(playlist_id, song_id):
    current_user = is_user_logged_in()
    # select playlist from database by user id and playlist id
    stmt = db.select(Playlist).filter_by(id=playlist_id,user_id=current_user.id)
    playlist = db.session.scalar(stmt)
    if playlist is None:
        return {'error': f'Playlist not found with id {playlist_id}'}, 404
    # select song from database by id
    stmt = db.select(Song).filter_by(id=song_id,playlist_id=playlist_id)
    song = db.session.scalar(stmt)

    if song and playlist:
        db.session.delete(song)
        db.session.commit()
        return {'message': f"Song '{song.name}' deleted successfully"}
    else:
        return {'error': f'Song not found with id {song_id}'}, 404

# updates playlist name
@playlist_bp.route('/<int:playlist_id>/', methods=['PUT', 'PATCH'])
@jwt_required()
def update_playlist(playlist_id):
    # selects playlist from db based on playlist id
    stmt = db.select(Playlist).filter_by(id=playlist_id)
    playlist = db.session.scalar(stmt)
    if playlist:
        playlist.name = request.json.get('name') or playlist.name
        db.session.commit()
        return PlaylistSchema().dump(playlist)
    else:
        return {'error': f'playlist not found with id {playlist_id}'}, 404

# deletes playlist from database
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
        return {'message': f"Playlist '{playlist.name}' deleted successfully"}
    else:
        return {'error': f'playlist not found with id {id}'}, 404
