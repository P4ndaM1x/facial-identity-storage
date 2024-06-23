import psycopg
from psycopg import sql


class DatabaseManager:
    def __init__(self, config, logger, init_script_path=None):
        self.config = config
        self.logger = logger
        self.init_script_path = init_script_path
        self.connection = None
        self.cursor = None

    def execute_script(self, script_path):
        try:
            with open(script_path, "r") as f:
                script = f.read()
        except Exception as e:
            self.logger.fatal(f"Error reading SQL script file: {e}")

        self.cursor.execute(script)
        self.connection.commit()
        self.logger.info("SQL script executed successfully")

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
            if self.init_script_path is not None:
                self.execute_script(self.init_script_path)
            self.execute_script
        except psycopg.Error as e:
            self.logger.error(e)
        self.logger.debug(f"Database version: {self.fetch_one('SELECT version();')}")

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
        
    def delete_person(self, name):
        try:
            self.execute_query("DELETE FROM person WHERE name = %s;", (name,))
            self.logger.info(f"Person {name} deleted from database.")
        except Exception as e:
            self.logger.error(f"Failed to delete person {name} from database. Error: {e}")

    def print_table_state(self):
        rows = self.fetch_all(f"SELECT * FROM person;")
        column_names = [desc[0] for desc in self.cursor.description]

        print("\nCurrent database state:")
        self.print_rows(rows, column_names)

    def print_person(self, name):
        rows = self.fetch_all(
            f"SELECT * FROM person WHERE name=%(name)s;", {"name": name}
        )
        column_names = [desc[0] for desc in self.cursor.description]

        print("Person data:")
        self.print_rows(rows, column_names)

    def print_closest_embeddings(self, sample_embedding):
        rows = self.fetch_all(f"SELECT * FROM person;")
        column_names = [desc[0] for desc in self.cursor.description]
        search_closest_query = sql.SQL(
            f"SELECT *, %s <-> embedding as distance FROM person ORDER BY embedding <-> %s LIMIT 5;"
        )
        rows = self.fetch_all(
            search_closest_query, (sample_embedding, sample_embedding)
        )

        print("\nDistance to the sample embedding:")
        self.print_rows(rows, column_names)

    def print_rows(self, rows=[], column_names=[], max_chars=16):
        column_names_formatted = "| ".join(
            [f"{name:{max_chars}}" for name in column_names]
        )
        row_length = len(column_names_formatted)
        spacer = row_length * "-"

        rows_formatted = [
            "| ".join([f"{str(value)[:max_chars]:{max_chars}}" for value in row])
            for row in rows
        ]

        print(spacer)
        print(column_names_formatted)
        print(spacer)
        for row in rows_formatted:
            print(row)
        print(spacer)
