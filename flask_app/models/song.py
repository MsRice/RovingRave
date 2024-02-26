from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Song:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.artist = data['artist']
        self.length = data['length']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    @staticmethod
    def new_song_validation(reg_form):
        is_Valid = True

        if len(reg_form['title']) < 3:
            flash("The title must be greater than 3 characters")
            is_Valid = False
        if len(reg_form['artist']) < 2:
            flash("The artist name must be greater than 2 characters")
            is_Valid = False

        if not reg_form['length']:
            flash("Length may cannot be empty")
            is_Valid = False

        return is_Valid

    @classmethod
    def add_new_song(cls, data):
        query = "INSERT INTO songs (title , artist , length , user_id) VALUE (%(title)s, %(artist)s , %(length)s, %(user_id)s);"

        connectToMySQL('roving_rave').query_db(query, data)

    @classmethod
    def get_all_songs(cls):
        query = "SELECT songs.* , users.first_name , users.last_name FROM songs LEFT JOIN users ON  user_id= users.id; "

        results = connectToMySQL('roving_rave').query_db(query)

        return results

    @classmethod
    def delete_song(cls, data):
        query = "DELETE FROM songs WHERE id = %(id)s;"

        connectToMySQL('roving_rave').query_db(query, data)
