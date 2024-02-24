from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask


class Song:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.title = data['title']
        self.artist = data['artist']
        self.length = data['length']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
