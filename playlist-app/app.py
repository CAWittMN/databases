from flask import Flask, redirect, render_template, url_for, flash
from flask_debugtoolbar import DebugToolbarExtension
import os

from models import db, connect_db, Playlist, Song, Playlist_Song, find_not_included
from forms import SongToPlaylistForm, SongForm, PlaylistForm

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


with app.app_context():
    connect_db(app)
    db.create_all()


# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)


@app.route("/")
def root():
    """Homepage: redirect to /playlists."""

    return redirect(url_for("show_all_playlists"))


##############################################################################
# Playlist routes


@app.route("/playlists")
def show_all_playlists():
    """Return a list of playlists."""

    playlists = Playlist.query.all()
    return render_template("/playlists.html", playlists=playlists)


@app.route("/playlists/<int:playlist_id>")
def show_playlist(playlist_id):
    """Show detail on specific playlist."""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = SongToPlaylistForm()
    return render_template("playlist.html", playlist=playlist, form=form)


@app.route("/playlists/add", methods=["GET", "POST"])
def add_playlist():
    """Handle add-playlist form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-playlists
    """
    form = PlaylistForm()

    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        new_playlist = Playlist.add_playlist(title=title, description=description)
        flash("Added playlist!")
        return redirect(url_for("show_all_playlists"))

    return render_template("new_playlist.html", form=form)


@app.route("/playlists/<int:playlist_id>/delete", methods=["POST"])
def delete_playlist(playlist_id):
    """Delete a playlist"""
    playlist = Playlist.query.get_or_404(playlist_id)
    db.session.delete(playlist)
    db.session.commit()
    flash("Deleted playlist!")

    return redirect(url_for("show_all_playlists"))


@app.route("/playlists/<int:playlist_id>/add-songs", methods=["GET", "POST"])
def add_songs_to_playlist(playlist_id):
    """add a song to the playlist"""

    playlist = Playlist.query.get_or_404(playlist_id)
    form = SongToPlaylistForm()
    curr_songs = [s.id for s in playlist.songs]
    choices = (
        db.session.query(Song.id, Song.title, Song.artist)
        .filter(Song.id.notin_(curr_songs))
        .all()
    )
    form.selection.choices = [(s.id, s.title + " ---- " + s.artist) for s in choices]

    if form.validate_on_submit():
        song = Song.query.get_or_404(form.selection.data)
        playlist.songs.append(song)
        db.session.add(playlist)
        db.session.commit()
        flash("Added song to playlist!")
        return redirect(url_for("show_playlist", playlist_id=playlist_id))

    return render_template("add_song_to_playlist.html", playlist=playlist, form=form)


##############################################################################
# Song routes


@app.route("/songs")
def show_all_songs():
    """Show list of songs."""

    songs = Song.query.order_by("artist").all()
    return render_template("songs.html", songs=songs)


@app.route("/songs/<int:song_id>", methods=["GET", "POST"])
def show_song(song_id):
    """return a specific song"""
    song = Song.query.get_or_404(song_id)
    form = SongToPlaylistForm()
    curr_playlists = [p.id for p in song.playlists]
    choices = (
        db.session.query(Playlist.id, Playlist.title)
        .filter(Playlist.id.notin_(curr_playlists))
        .all()
    )
    form.selection.choices = [(p.id, p.title) for p in choices]

    if form.validate_on_submit():
        playlist = Playlist.query.get_or_404(form.selection.data)
        song.playlists.append(playlist)
        db.session.add(song)
        db.session.commit()
        return redirect(url_for("show_song", song_id=song_id))

    return render_template("song.html", song=song, form=form)


@app.route("/songs/add", methods=["GET", "POST"])
def add_song():
    """Handle add-song form:

    - if form not filled out or invalid: show form
    - if valid: add playlist to SQLA and redirect to list-of-songs
    """

    form = SongForm()

    if form.validate_on_submit():
        title = form.title.data
        artist = form.artist.data

        new_song = Song.add_song(title=title, artist=artist)

        flash("Added song!")

        return redirect(url_for("show_song", song_id=new_song.id))

    return render_template("new_song.html", form=form)


@app.route("/playlists/<int:playlist_id>/remove/<int:song_id>", methods=["POST"])
def remove_song_from_playlist(playlist_id, song_id):
    """Remove a song from the playlist"""

    playlist = Playlist.query.get_or_404(playlist_id)
    song = Song.query.get_or_404(song_id)
    song.playlists.remove(playlist)

    db.session.add(song)
    db.session.commit()

    flash("Removed song from plalist!")

    return redirect(url_for("show_playlist", playlist_id=playlist_id))


@app.route("/songs/<int:song_id>/delete", methods=["POST"])
def delete_song(song_id):
    """Delete a song"""
    song = Song.query.get_or_404(song_id)
    db.session.delete(song)
    db.session.commit()
    flash("Deleted song!")
    return redirect(url_for("show_all_songs"))
