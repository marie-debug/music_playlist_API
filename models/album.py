from init import db, ma


class AlbumSchema(ma.Schema):

    class Meta:
        # Fields to expose
        fields = ("id", "title", "artist")


class Album(db.Model):
    __tablename__ = 'albums'

    id = db.Column(db.Integer, primary_key=True)
    title  = db.Column(db.String(100))
    artist = db.Column(db.String(50))
    songs = db.relationship("song", back_populates= "album")

 