from mysql.connector import connect
from pprint import pprint


class DatabaseConnector:
    def __init__(self, host, user, password, database):
        self.connection = connect(host=host, database=database, user=user, password=password)
        self.query = self.connection.cursor()
        self.is_connected = self.connection.is_connected();

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            self.query.close()

    def execute(self, query: str):
        self.query.execute(query)
        return self.query.fetchall()

    def insert(self, query: str):
        response = self.execute(query)
        self.connection.commit()
        return response

    def dump(self, query: str):
        self.query.execute(query)
        response = [dict((self.query.description[i][0], value) for i, value in enumerate(row)) for row in
                    self.query.fetchall()]
        pprint(response)

    def call_procedure(self, name: str, arguments: list = tuple()):
        self.query.callproc(name, arguments)
        for result in self.query.stored_results():
            print(result.fetchall())

    def create_procedure(self, query: str):
        pass
