from init import db, ma



class SongSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name","genre")
song_schema = SongSchema(many=True)


class Song(db.Model):
    __tablename__ = 'songs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genre = db.Column(db.String)
  