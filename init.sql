CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS person (
  id SERIAL PRIMARY KEY,
  person_id BIGINT UNIQUE NOT NULL,
  name TEXT UNIQUE NOT NULL,
  date_of_birth DATE, -- format yyyy-mm-dd
  place_of_birth TEXT,
  phone_number TEXT,
  lib_card_exp_date DATE, -- format yyyy-mm-dd
  bicycle_card_no INT,
  embedding vector,
  created_at timestamptz DEFAULT now()
);