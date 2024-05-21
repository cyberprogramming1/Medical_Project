import hashlib
import pyodbc

class RegisterSystem:
    def __init__(self, connection):
        self.connection = connection

    def register_user(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, hashed_password))
            self.connection.commit()
            cursor.close()
            print("User registered successfully.")
        except pyodbc.Error as e:
            print(f"Error registering user: {e}")
