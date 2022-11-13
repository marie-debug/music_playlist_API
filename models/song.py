from init import db, ma


class SongSchema(ma.Schema):
    
    class Meta:
        # Fields to expose
        fields = ("id", "name", "genre", "playlist_id")


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    genre = db.Column(db.String(50))

    playlist_id = db.Column(db.Integer, db.ForeignKey("playlists.id"))

    playlists = db.relationship("Playlist", back_populates="songs")

    # artist = db.relationship(
    #     "Artist", back_populates="songs", cascade='all, delete')
