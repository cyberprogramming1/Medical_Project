import hashlib
import pyodbc

class LoginSystem:
    def __init__(self, connection):
        self.connection = connection
        self.logged_in_user = None

    def login_user(self, username, password):
        try:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            cursor = self.connection.cursor()
            cursor.execute("SELECT Password FROM Users WHERE Username = ?", (username,))
            stored_password = cursor.fetchone()
            if stored_password and hashed_password == stored_password[0]:
                print("Login successful.")
                self.logged_in_user = username
                return True
            else:
                print("Invalid username or password.")
                return False
        except pyodbc.Error as e:
            print(f"Error logging in: {e}")

    def is_authenticated(self):
        return self.logged_in_user is not None

    def logout(self):
        self.logged_in_user = None
        print("Logged out successfully.")
