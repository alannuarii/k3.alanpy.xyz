from app.conn import cur, conn
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def set_password(self, password:str):
        password_hash = generate_password_hash(password)
        return password_hash

    def check_password(self, password_hash:str, password:str):
        return check_password_hash(password_hash, password)

    def register(self, name, email, username, password):
        cur.execute(f"INSERT INTO user (name, email, username, password) VALUES ('{name}', '{email}', '{username}', '{password}')")
        conn.commit()

    def get_user(self, username:str):
        cur.execute(f"SELECT * FROM user WHERE username = '{username}'")
        result = cur.fetchone()
        return result
