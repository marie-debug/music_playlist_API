from init import db, ma
from marshmallow import fields
from helpers import validate


class UserSchema(ma.Schema):

    email = fields.Email()
   
    firstname = validate(3,100,'firstname')
    lastname = validate(3,100,'lastname')
    password = fields.String(required=True)

    class Meta:
        fields = ('id', 'firstname', 'lastname',
                  'email', 'password', 'is_admin')
        ordered = True


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    playlists = db.relationship("Playlist", back_populates="user")
