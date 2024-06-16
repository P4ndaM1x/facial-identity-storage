CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS person (
  id SERIAL PRIMARY KEY,
  name TEXT UNIQUE NOT NULL,
  address TEXT,
  phone_number TEXT,
  bicycle_card_id BIGINT,
  student_card_id BIGINT,
  student_class TEXT,
  embedding vector,
  created_at timestamptz DEFAULT now()
);