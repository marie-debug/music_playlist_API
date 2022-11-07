from init import db, ma



class PlaylistSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "playlist_name", "creation_date")
playlist_schema = PlaylistSchema(many=True)


class Playlist(db.Model):
    __tablename__ = 'playlists'

    id = db.Column(db.Integer, primary_key=True)
    playlist_name = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.Date)