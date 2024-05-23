CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS person (
  id SERIAL PRIMARY KEY,
  name text UNIQUE,
  embedding vector,
  created_at timestamptz DEFAULT now()
);