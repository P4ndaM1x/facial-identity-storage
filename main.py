from src.ArgParser import initArgs
from src.ConfigParser import initConfig
from src.Logger import initLogger
from src.EmbeddingExtractor import EmbeddingExtractor
from src.DatabaseManager import DatabaseManager
from src.DocumentScanner import DocumentScanner
from src.FaceExtractor import FaceExtractor

from PIL import Image
from pathlib import Path
from psycopg import sql
import numpy as np
import os
import cv2

PHOTOS_DIR = Path("images/generated")
CONFIG_PATH = Path("./src/config/config.ini")


def find_files(filenames, root_dir=Path(".")):
    matching_files = []
    for dirpath, _, files in os.walk(root_dir):
        for filename in files:
            if filename in filenames:
                matching_files.append(os.path.join(dirpath, filename))
    return matching_files


class Application:
    def __init__(self, args, config, logger):
        self.args = args
        self.logger = logger
        self.db_manager = DatabaseManager(
            config, logger, config.get("DATABASE", "initScriptPath")
        )
        self.embedding_extractor = EmbeddingExtractor()
        self.face_extractor = FaceExtractor()
        self.document_scanner = DocumentScanner()

    def run(self):
        # Connect to the database
        self.db_manager.connect()
        self.logger.debug(
            f"Database version: {self.db_manager.fetch_one('SELECT version();')}"
        )

        # Clear the database if the --clearDatabase flag is set
        if self.args.clearDatabase:
            self.logger.info("Clearing person table")
            self.db_manager.clear_table("person")

        if self.args.initDatabase:
            self.logger.info("Initializing database")

            file_paths = find_files(["university_card.png", "bicycle_card.png"])

            for file_path in file_paths:
                self.scan_document(file_path)

        self.db_manager.print_table_state()

        # Scan the person data from document if the --documentPhoto flag is set
        if self.args.documentPhotoPath:
            name = self.scan_document(self.args.documentPhotoPath)
            self.db_manager.print_person(name)

        # Extract embeddings from photos and insert them into the database
        self.db_manager.print_table_state()
        # self.db_manager.print_closest_embeddings()

        # Close the database connection
        self.db_manager.close()

    def scan_document(self, document_path):
        face_img = self.face_extractor.get_photo(document_path)
        face_embedding = self.embedding_extractor.vectorize(face_img).as_str()

        scanned_data = self.document_scanner.recognize_card_type(document_path)

        insert_query = """
            INSERT INTO person (name, address, phone_number, bicycle_card_id, student_card_id, student_class, embedding)
            VALUES (%(name)s, %(address)s, %(phone_number)s, %(bicycle_card_id)s, %(student_card_id)s, %(student_class)s, %(embedding)s)
            ON CONFLICT (name) DO UPDATE
            SET 
                bicycle_card_id = COALESCE(person.bicycle_card_id, EXCLUDED.bicycle_card_id),
                student_card_id = COALESCE(person.student_card_id, EXCLUDED.student_card_id),
                student_class = COALESCE(person.student_class, EXCLUDED.student_class)
            WHERE 
                person.bicycle_card_id IS NULL 
                OR person.student_card_id IS NULL 
                OR person.student_class IS NULL
            RETURNING id;
        """

        scanned_data["embedding"] = face_embedding
        self.db_manager.execute_query(insert_query, scanned_data)
        return scanned_data["name"]


def main():
    args = initArgs()
    config = initConfig(CONFIG_PATH)
    logger = initLogger()
    app = Application(args, config, logger)
    app.run()


if __name__ == "__main__":
    main()
