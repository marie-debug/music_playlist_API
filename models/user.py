from init import db, ma

class UserSchema(ma.Schema):
    
   class Meta:
        # Fields to expose
        fields = ("id", "firstname", "lastname", "email", "is_admin", "password")



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    playlists= db.relationship("Playlist",back_populates="user")
  


