from cli.ArgParser import *
from cli.ConfigParser import *
from cli.Logger import *
from cli.EmbeddingExtractor import *
from cli.scanner import *

import psycopg
import numpy as np
from psycopg import sql
from PIL import Image
from pathlib import Path

PHOTOS_DIR = Path("images/generated") 

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

class EmbeddingService:
    def __init__(self, extractor):
        self.extractor = extractor

    def extract_embeddings(self, photos_dir):
        filenames = os.listdir(photos_dir)
        embeddings = []
        for photo_name in filenames:
            img = Image.open(os.path.join(photos_dir, photo_name))
            embedding = self.extractor.vectorize(img).str()
            embeddings.append((photo_name, embedding))
        return embeddings

class Application:
    def __init__(self, args, config, logger):
        self.args = args
        self.logger = logger
        self.db_manager = DatabaseManager(config, logger)
        self.embedding_service = EmbeddingService(EmbeddingExtractor())

    def run(self):
        # Connect to the database
        self.db_manager.connect()
        self.db_manager.fetch_one("SELECT version();")
        self.logger.debug(f"Database version: {self.db_manager.cursor.fetchone()}")

        # Clear the database if the --clearDatabase flag is set
        if self.args.clearDatabase:
            self.logger.debug("Clearing person table")
            self.db_manager.clear_table("person")
            
        # Scan the person data from document if the --documentPhoto flag is set
        if(self.args.documentPhoto):
            person_info = DocumentScanner().recognize_card_type(self.args.documentPhoto)
            print("Person info: ", person_info)

        # Extract embeddings from photos and insert them into the database
        person_vec = self.embedding_service.extract_embeddings(PHOTOS_DIR)
        insert_query = sql.SQL("INSERT INTO person (name, embedding) VALUES (%s, %s)")

        for person, vec in person_vec:
            self.db_manager.execute_query(insert_query, (person, vec))

        # Print the current state of the database
        self.print_database_state()
        self.print_closest_embeddings()

        # Close the database connection
        self.db_manager.close()

    def print_database_state(self):
        rows = self.db_manager.fetch_all("SELECT * FROM person;")
        column_names = [desc[0] for desc in self.db_manager.cursor.description]
        print("Current database state:")
        for row in rows:
            print(f"({column_names[0]}: {row[0]}, {column_names[1]}: {row[1]}, {column_names[2]}: {row[2][:80]}...)")

    def print_closest_embeddings(self):
        rows = self.db_manager.fetch_all("SELECT * FROM person;")
        column_names = [desc[0] for desc in self.db_manager.cursor.description]
        sample_embedding = rows[0][2]
        search_closest_query = sql.SQL(
            "SELECT *, %s <-> embedding as distance FROM person ORDER BY embedding <-> %s LIMIT 5;"
        )
        rows = self.db_manager.fetch_all(search_closest_query, (sample_embedding, sample_embedding))

        print("\nDistance to the sample embedding:")
        for row in rows:
            print(f"({column_names[0]}: {row[0]}, {column_names[1]}: {row[1]}, {column_names[2]}: {row[2][:80]}..., distance: {row[-1]})")

def main():
    args = initArgs()
    config = initConfig(args.configFile.name)
    logger = initLogger()
    app = Application(args, config, logger)
    app.run()

if __name__ == "__main__":
    main()