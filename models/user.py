# from main import db
# from sqlalchemy.sql import func



# class User(db.Model):
#     __tablename__ = 'users'

#     id = db.Column(db.Integer, primary_key=True)
#     firstname = db.Column(db.String(100), nullable=False)
#     lastname = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(80), unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     is_admin = db.Column(db.Boolean, default=False)
#     # created_at = db.Column(db.DateTime(timezone=True),
#     #                        server_default=func.now())

#     # cards = db.relationship('Card', back_populates='user', cascade='all, delete')
    # comments = db.relationship('Comment', back_populates='user', cascade='all, delete')

