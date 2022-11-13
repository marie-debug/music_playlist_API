from init import db, ma
from marshmallow import fields


class PlaylistSchema(ma.Schema):

    songs = fields.List(fields.Nested('SongSchema'))

    class Meta:
        fields = ("id", "name", "creation_date", "user_id", "songs")
        ordered = True


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", back_populates="playlists")

    songs = db.relationship("Song", back_populates="playlists", cascade="all, delete-orphan")
