from init import db, ma


class ArtistSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "genre")


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genre = db.Column(db.String)
    # song_id = db.Column(db.Integer, db.ForeignKey(
    #     "songs.id", ondelete="CASCADE"))

    # songs = db.relationship("Song", back_populates="artists")
