from flask import Blueprint
from init import db, bcrypt
from models.user import User



db_commands = Blueprint('db', __name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("Tables created")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped")

@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            firstname = 'marion',
            lastname = 'akinyi',
            email='admin@spam.com',
            password=bcrypt.generate_password_hash('foobar231').decode("utf-8"),
            is_admin=True
        )
    ]

    db.session.add_all(users)
    db.session.commit()


