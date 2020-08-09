import psycopg2


class DatabaseTools:

    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password

    def get_connection(self):
        """ Establishes connection to database """
        conn = psycopg2.connect(host=self.host,
                                database=self.database,
                                user=self.user,
                                password=self.password)
        return conn
