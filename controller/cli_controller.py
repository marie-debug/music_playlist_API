from flask import Blueprint
from init import db, bcrypt
from models.user import User
from datetime import date
from models.song import Song
from models.playlist import Playlist


db_commands = Blueprint('db', __name__)


@db_commands.cli.command('create')
def create_db():
    db.create_all()
    print("Tables created")


@db_commands.cli.command('drop')
def drop_db():
    db.drop_all()
    print("Tables dropped")


@db_commands.cli.command('seed')
def seed_db():
    users = [
        User(
            firstname='marion',
            lastname='akinyi',
            email='admin@spam.com',
            password=bcrypt.generate_password_hash(
                'foobar231').decode("utf-8"),
            is_admin=True
        )
    ]

    db.session.add_all(users)
    db.session.commit()

    playlists = [
        Playlist(

            playlist_name='test_playlist',
            creation_date=date.today(),
            user=users[0]


        )

    ]

    db.session.add_all(playlists)
    db.session.commit()

    songs = [
        Song(
            name='test_song',
            genre='test_genre',
            playlist_id=1
        )

    ]

    db.session.add_all(songs)
    db.session.commit()
    print('Tables seeded')
