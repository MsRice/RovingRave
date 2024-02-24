# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def registration_validation(reg_form):
        is_Valid = True
        if len(reg_form['first_name']) < 2:
            flash("Your first name must be greater than 2 characters")
            is_Valid = False

        if len(reg_form['last_name']) < 2:
            flash("Your last name must be greater than 2 characters")
            is_Valid = False

        if not EMAIL_REGEX.match(reg_form['email']):
            flash("Invalid email address!")
            is_Valid = False

        if reg_form['password'] != reg_form['conf_password']:
            flash("Check password match!")
            is_Valid = False

        return is_Valid

    @classmethod
    def register(cls, data):
        query = "INSERT INTO users (first_name , last_name , email , password) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s);"

        connectToMySQL('pies_schema').query_db(query, data)

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        result = connectToMySQL("pies_schema").query_db(query, data)

        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
