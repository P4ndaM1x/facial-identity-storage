from ArgParser import *
from ConfigParser import *
from Logger import *
from EmbeddingExtractor import *

import psycopg
import numpy as np
from psycopg import sql
from PIL import Image


def main():
    args = initArgs()
    config = initConfig(args.configFile.name)
    logger = initLogger()

    embeddingExtractor = EmbeddingExtractor()
    cursor = None
    connection = None
    try:
        connection = psycopg.connect(
            host=config.get("DATABASE", "host"),
            port=config.get("DATABASE", "port"),
            dbname=config.get("DATABASE", "name"),
            user=config.get("DATABASE", "user"),
            password=config.get("DATABASE", "password"),
        )
        logger.info("Database connection established")

        cursor = connection.cursor()
        cursor.execute("SELECT version();")
        logger.debug(f"Database version: {cursor.fetchone()}")

        if args.clearDatabase:
            logger.debug("Clearing person table")
            try:
                cursor.execute("DELETE FROM person;")
            except psycopg.Error as e:
                logger.error(e)
            finally:
                connection.commit()

        person_vec = None
        filenames = os.listdir(args.photosDir)
        for photo_name in filenames:
            person_img = [
                (photo, Image.open(os.path.join(args.photosDir, photo)))
                for photo in filenames
            ]
            person_vec = [
                (person, embeddingExtractor.vectorize(img).str())
                for person, img in person_img
            ]

        try:
            insert_query = sql.SQL(
                "INSERT INTO person (name, embedding) VALUES (%s, %s)",
            )
            [cursor.execute(insert_query, (person, vec)) for person, vec in person_vec]
        except psycopg.Error as e:
            logger.error(e)
        finally:
            connection.commit()

        cursor.execute("SELECT * FROM person;")
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        print("Current database state:")
        for row in rows:
            print(
                f"({column_names[0]}: {row[0]}, {column_names[1]}: {row[1]}, {column_names[2]}: {row[2][:80]}...)"
            )

        search_closest_query = sql.SQL(
            "SELECT *, %s <-> embedding as distance FROM person ORDER BY embedding <-> %s LIMIT 5;"
        )
        sample_embedding = rows[0][2]
        cursor.execute(search_closest_query, (sample_embedding, sample_embedding))
        rows = cursor.fetchall()

        print("\nDistance to the sample embedding:")
        for row in rows:
            print(
                f"({column_names[0]}: {row[0]}, {column_names[1]}: {row[1]}, {column_names[2]}: {row[2][:80]}..., distance: {row[-1]})"
            )

    except psycopg.Error as e:
        logger.error(e)
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()
        logger.info("Database connection closed")


if __name__ == "__main__":
    main()
