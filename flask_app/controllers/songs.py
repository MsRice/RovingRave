from flask_app import app
from flask import render_template, redirect, request, session

from flask_app.models.song import Song
from flask_app.models.user import User
from flask_app.models.user_type import Type


from flask_app.controllers.users import is_logged_in


@app.route('/crowd_wall')
def song_wall():
    if is_logged_in():
        user_info = session['user_info']
        return render_template("crowd_wall.html", user_info=user_info)
    else:
        return redirect('/')


@app.route('/add_song', methods=['POST'])
def add_song():
    # validation form here
    data = {
        'user_id': request.form['user_id'],  # Suggester
        'title': request.form['title'],
        'artist': request.form['artist'],
        'length': request.form['length']
    }

    # Song insert here

    return redirect('/crowd_wall')


@app.route('/dj_wall')
def dj_wall():
    if is_logged_in():
        user_info = session['user_info']
        return render_template("dj_wall.html", user_info=user_info)
    else:
        return redirect('/')
