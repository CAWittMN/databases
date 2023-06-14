"""Forms for playlist app."""

from wtforms import SelectField, StringField, TextAreaField
from flask_wtf import FlaskForm
from wtforms.validators import Length, InputRequired


class PlaylistForm(FlaskForm):
    """Form for adding playlists."""

    name = StringField(
        "Name",
        validators=[
            Length(max=20, message="Playlist name is too long"),
            InputRequired(),
        ],
    )
    description = TextAreaField(
        "Description",
        validators=[
            Length(max=255, message="Playlist description is too long"),
            InputRequired(),
        ],
    )


class SongForm(FlaskForm):
    """Form for adding songs."""

    title = StringField(
        "Title",
        validators=[
            Length(max=20, message="Song title is too long"),
            InputRequired(),
        ],
    )
    artist = StringField(
        "Artist",
        validators=[
            Length(max=20, message="Artist name is too long"),
            InputRequired(),
        ],
    )


class NewSongForPlaylistForm(FlaskForm):
    """Form for adding a song to playlist."""

    song = SelectField("Song To Add", coerce=int)
