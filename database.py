import pyodbc

class Database:
    def __init__(self, server, database):
        self.server = server
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = pyodbc.connect(f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.server};DATABASE={self.database};Trusted_Connection=yes;')
            print('Connected to Database.')
        except pyodbc.Error as e:
            print(f"Error connecting to database: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print('Disconnected from Database.')
        else:
            print('No active connection to disconnect.')
