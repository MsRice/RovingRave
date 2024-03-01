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

        connectToMySQL('roving_rave_schema').query_db(query, data)

        query1 = "SELECT id FROM songs \
            WHERE title = %(title)s \
                ORDER BY created_at DESC \
                    LIMIT 1"

        song_id = connectToMySQL('roving_rave_schema').query_db(query1, data)

        data['song_id'] = song_id[0]['id']

        query2 = "INSERT INTO crowd_queue (song_id , user_id) VALUE ( %(song_id)s , %(user_id)s) "
        connectToMySQL('roving_rave_schema').query_db(query2, data)

    @classmethod
    def get_all_crowd_songs(cls):
        query = "SELECT * , users.first_name , users.last_name FROM crowd_queue \
            LEFT JOIN songs ON song_id = songs.id \
             LEFT JOIN users ON  crowd_queue.user_id = users.id ;"

        results = connectToMySQL('roving_rave_schema').query_db(query)

        return results

    @classmethod
    def delete_song(cls, data):

        query = "DELETE FROM songs WHERE id = %(id)s;"
        connectToMySQL('roving_rave_schema').query_db(query, data)

    @classmethod
    def delete_song_from_crowd(cls, data):
        query = "DELETE FROM crowd_queue WHERE id = %(crowd_id)s;"
        connectToMySQL('roving_rave_schema').query_db(query, data)

    @classmethod
    def delete_song_from_queue(cls, data):
        query = "DELETE FROM queues WHERE id = %(id)s;"
        connectToMySQL('roving_rave_schema').query_db(query, data)

    @classmethod
    def add_to_queue(cls, data):
        query = "INSERT INTO queues (user_id ,song_id) VALUES (%(user_id)s , %(id)s );"

        connectToMySQL('roving_rave_schema').query_db(query, data)

    @classmethod
    def get_queue(cls):
        query = "SELECT * FROM queues \
        left join songs ON song_id = songs.id \
        left JOIN users ON queues.user_id = users.id;"

        results = connectToMySQL('roving_rave_schema').query_db(query)

        return results

    @classmethod
    def get_song_from_queue(cls, data):
        query = "SELECT * FROM queues \
            LEFT JOIN songs ON songs.id = song_id \
            LEFT JOIN users ON queues.user_id = users.id \
            WHERE queues.id = %(id)s ; "

        results = connectToMySQL('roving_rave_schema').query_db(query, data)

        return results

    @classmethod
    def add_to_current(cls, data):
        query = "INSERT INTO current_song (user_id ,song_id) VALUES (%(user_id)s , %(song_id)s );"

        connectToMySQL('roving_rave_schema').query_db(query, data)

    @classmethod
    def get_current(cls):
        query = "SELECT * FROM current_song \
        left join songs ON song_id = songs.id \
        left JOIN users ON current_song.user_id = users.id \
        order by current_song.created_at desc \
        limit 1;"

        results = connectToMySQL('roving_rave_schema').query_db(query)

        return results
