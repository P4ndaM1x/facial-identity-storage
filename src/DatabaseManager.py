import psycopg
from psycopg import sql

class DatabaseManager:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg.connect(
                host=self.config.get("DATABASE", "host"),
                port=self.config.get("DATABASE", "port"),
                dbname=self.config.get("DATABASE", "name"),
                user=self.config.get("DATABASE", "user"),
                password=self.config.get("DATABASE", "password"),
            )
            self.logger.info("Database connection established")
            self.cursor = self.connection.cursor()
        except psycopg.Error as e:
            self.logger.error(e)

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
        self.logger.info("Database connection closed")

    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except psycopg.Error as e:
            self.logger.error(e)
            self.connection.rollback()

    def fetch_all(self, query, params=None):
        self.execute_query(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.execute_query(query, params)
        return self.cursor.fetchone()

    def clear_table(self, table_name):
        self.execute_query(f"DELETE FROM {table_name};")

    def print_table_state(self):
        rows = self.fetch_all(f"SELECT * FROM person;")
        column_names = [desc[0] for desc in self.cursor.description]

        print("Current database state:")
        self.print_rows(rows, column_names)

    def print_closest_embeddings(self, sample_embedding):
        rows = self.fetch_all(f"SELECT * FROM person;")
        column_names = [desc[0] for desc in self.cursor.description]
        search_closest_query = sql.SQL(
            f"SELECT *, %s <-> embedding as distance FROM person ORDER BY embedding <-> %s LIMIT 5;"
        )
        rows = self.fetch_all(search_closest_query, (sample_embedding, sample_embedding))

        print("\nDistance to the sample embedding:")
        self.print_rows(rows, column_names)
    
    def print_rows(self, rows=[], column_names=[], max_chars=15):
        column_names_formatted = "| ".join([f"{name:{max_chars}}" for name in column_names])
        self.logger.info(column_names_formatted)

        rows_formatted = ['| '.join([f"{str(value)[:max_chars]:{max_chars}}" for value in row]) for row in rows]
        for row in rows_formatted:
            self.logger.info(row)
