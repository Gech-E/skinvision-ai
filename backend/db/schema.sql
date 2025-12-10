CREATE TABLE IF NOT EXISTS prediction_results (
    id SERIAL PRIMARY KEY,
    image_path TEXT,
    predicted_class TEXT NOT NULL,
    confidence REAL NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
