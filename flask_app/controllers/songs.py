from flask_app import app
from flask import render_template, redirect, request, session

from flask_app.models.song import Song
from flask_app.models.user import User
from flask_app.models.user_type import Type
from flask_app.models.spotify import search_for_song_and_artist
from datetime import timedelta

from flask_app.controllers.users import is_logged_in


@app.route('/crowd_wall')
def song_wall():
    if is_logged_in():
        user_info = session['user_info']
        crowd_songs = Song.get_all_crowd_songs()
        playing_song = Song.get_current()
        return render_template("crowd_wall.html", user_info=user_info, crowd_songs=crowd_songs, playing_song=playing_song)
    else:
        return redirect('/')


@app.route('/add_song', methods=['POST'])
def add_song():

    if not Song.new_song_validation(request.form):
        return redirect('/crowd_wall')
    else:

        spotify_data = search_for_song_and_artist(
            request.form['artist'], request.form['title'])

        duration_ss = timedelta(seconds=(spotify_data['duration'] / 1000))
        data = {
            'user_id': request.form['user_id'],  # Suggester
            'title': spotify_data['title'],
            'artist': spotify_data['artist_names'],
            'length': duration_ss,
            'cover_link': spotify_data['cover_link'],
            'track_link': spotify_data['track_link'],
            'spot_id': spotify_data['spot_id']
        }

        Song.add_new_song(data)

        return redirect('/crowd_wall')


@app.route('/dj_wall')
def dj_wall():
    if is_logged_in():
        user_info = session['user_info']
        crowd_songs = Song.get_all_crowd_songs()
        all_queue = Song.get_queue()
        playing_song = Song.get_current()

        print("playing_song -->>", playing_song[0]['track_link'])
        return render_template("dj_wall.html", user_info=user_info, crowd_songs=crowd_songs, all_queue=all_queue, playing_song=playing_song)
    else:
        return redirect('/')


@app.route('/delete_song', methods=['POST'])
def delete_song():
    data = {
        'id': request.form['song_id'],
        'crowd_id': request.form['crowd_id']
    }
    Song.delete_song_from_crowd(data)
    Song.delete_song(data)
    return redirect('/crowd_wall')


@app.route('/add_to_queue', methods=['POST'])
def add_to_queue():
    data = {
        'id': request.form['song_id'],
        'crowd_id': request.form['crowd_id'],
        'user_id': request.form['user_id']
    }

    Song.add_to_queue(data)
    Song.delete_song_from_crowd(data)

    return redirect('/dj_wall')


@app.route('/play_button', methods=['POST'])
def play_button():
    data = {
        'id': request.form['crowd_id'],
        'song_id': request.form['song_id'],
        'user_id': request.form['user_id']
    }

    Song.delete_song_from_queue(data)
    Song.add_to_current(data)

    return redirect("/dj_wall")
