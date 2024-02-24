from flask_app import app
from flask import render_template, redirect, request, session

from flask_app.models.song import Song
from flask_app.models.user import User
from flask_app.models.user_type import Type


from flask_app.controllers.users import is_logged_in


@app.route('/song_wall')
def song_wall():
    if is_logged_in():
        return render_template("song_wall.html")
    else:
        return redirect('/')
