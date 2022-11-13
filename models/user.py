from init import db, ma
from flask_marshmallow import fields
from marshmallow import  fields, validate

class UserSchema(ma.Schema):

    class Meta:

        email = fields.Email()
        firstname = fields.Str(required=True,validate=validate.Length(min=1,max=100),error_messages={"required": "firstname is required."})
        lastname = fields.Str(required=True,validate=validate.Length(min=1,max=100),error_messages={"required": "firstname is required."})
        password = fields.Str(required=True, allow_none=True)


        fields = ('id', 'firstname','lastname', 'email', 'password', 'is_admin')


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    playlists = db.relationship("Playlist", back_populates="user")
