import torch
import torchvision
import torchvision.models as models
import psycopg
import numpy as np
from psycopg import sql
from PIL import Image

class ResNetEncoder(torch.nn.Module):
    def __init__(self):
        super(ResNetEncoder, self).__init__()
        original = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)
        self.features = torch.nn.Sequential(*list(original.children())[:-1])
    
    def forward(self, x):
        x = self.features(x)
        x = torch.flatten(x, 1)
        return x

class ImageVectorizer():

    def __init__(self):
        self.transforms = torchvision.transforms.Compose([
            torchvision.transforms.Resize(256),
            torchvision.transforms.CenterCrop(224),
            torchvision.transforms.ToTensor(),
            torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.encoder = ResNetEncoder()
        self.result = None

    def vectorize(self, image):
        t_img = self.transforms(image)

        with torch.no_grad():
            res = self.encoder(t_img.unsqueeze(0))
            self.result = res.flatten().tolist()
            return self

    def str(self):
        return "[" + ",".join([str(el) for el in self.result]) + "]"
    
    def get(self):
        return self.result

    def list_from_str(s):
        s = s.strip("[]")
        elements = s.split(",")
        result = [float(el) for el in elements]
        return result

DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'aoip'
DB_USER = 'postgres'
DB_PASSWORD = 'postgres'
PEOPLE = ["papiez", "chodakowska"]

vectorizer = ImageVectorizer()
cursor = None
conn = None
try:
    conn = psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    print("Database connection established.")

    cursor = conn.cursor()

    cursor.execute("SELECT version();")

    db_version = cursor.fetchone()
    print(f"Database version: {db_version}")

    insert_query = sql.SQL(
        "INSERT INTO person (name, embedding) VALUES (%s, %s)",
    )

    person_vec = None
    for person in PEOPLE:
        person_img = [(person, Image.open(person + ".jpg")) for person in PEOPLE]
        person_vec = [(person, vectorizer.vectorize(img).str()) for person, img in person_img]

    try: 
        [cursor.execute(insert_query, (person, vec)) for person, vec in person_vec]
    except psycopg.Error as e:
        print(f"Error: {e}")
    finally:
        conn.commit()

    print("\n")
    
    cursor.execute("SELECT * FROM person;")
    rows = cursor.fetchall()

    column_names = [desc[0] for desc in cursor.description]

    for row in rows:
        print(f"({column_names[0]}: {row[0]}, {column_names[1]}: {row[1]}, {column_names[2]}: {row[2][:80]}...)")

    print("\n")

    search_closest_query = sql.SQL(
        "SELECT *, %s <-> embedding as distance FROM person ORDER BY embedding <-> %s LIMIT 5;"
    )
    sample_embedding = rows[0][2]
    cursor.execute(search_closest_query, (sample_embedding, sample_embedding))

    rows = cursor.fetchall()

    for row in rows:
        print(f"({column_names[0]}: {row[0]}, {column_names[1]}: {row[1]}, {column_names[2]}: {row[2][:80]}..., distance: {row[-1]})")


except psycopg.Error as e:
    print(f"Error: {e}")
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
    print("Database connection closed.")
