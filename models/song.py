from init import db, ma
from helpers import validate

class SongSchema(ma.Schema):
    name = validate(3,100,'name')
    artist = validate(1,100,'artist')
    genre = validate(3,50,'genre')

    class Meta:
        # Fields to expose
        fields = ("id", "name", "genre", "playlist_id",'artist')


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(50))
    artist = db.Column(db.String(100))

    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"))

    playlists = db.relationship("Playlist", back_populates="songs")
    
