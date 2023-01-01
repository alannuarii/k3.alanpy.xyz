from app.conn import connection
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def set_password(self, password:str):
        password_hash = generate_password_hash(password)
        return password_hash

    def check_password(self, password_hash:str, password:str):
        return check_password_hash(password_hash, password)

    def register(self, name, email, username, password):
        query = f"INSERT INTO user (name, email, username, password) VALUES ('{name}', '{email}', '{username}', '{password}')"
        connection(query, 'insert')

    def get_user(self, username:str):
        query = f"SELECT * FROM user WHERE username = '{username}'"
        result = connection(query, 'selectone')
        return result
