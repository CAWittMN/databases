"""Models for Playlist app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Playlist(db.Model):
    """Playlist."""

    __tablename__ = "playlists"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False, unique=True)
    description = db.Column(db.String(250), nullable=False)

    songs = db.relationship("Song", secondary="playlists_songs", backref="playlists")

    @classmethod
    def add_playlist(cls, title, description):
        new_playlist = cls(title=title, description=description)
        db.session.add(new_playlist)
        db.session.commit()
        return new_playlist


class Playlist_Song(db.Model):
    """Mapping of a playlist to a song."""

    __tablename__ = "playlists_songs"

    playlist_id = db.Column(
        db.Integer,
        db.ForeignKey("playlists.id"),
        primary_key=True,
        nullable=False,
    )
    song_id = db.Column(
        db.Integer,
        db.ForeignKey("songs.id"),
        primary_key=True,
        nullable=False,
    )


class Song(db.Model):
    """Song."""

    __tablename__ = "songs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    artist = db.Column(db.String(50), nullable=False)

    @classmethod
    def add_song(cls, title, artist):
        new_song = cls(title=title, artist=artist)
        db.session.add(new_song)
        db.session.commit()
        return new_song


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
