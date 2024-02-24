from flask_app.config.mysqlconnection import connectToMySQL
from flask import Flask


class Type:
    def __init__(self, data):
        self.id = data['id']
        self.user_type = data['user_type']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
