# Skin Cancer Detection System Architecture

## High-Level Overview
- **Modeling**: EfficientNetB0 transfer learning pipeline executed in Google Colab. Handles HAM10000 ingestion, missing values, label encoding, augmentation, class weights, training, evaluation, and artifact export (`model.h5`, `label_map.json`, `preprocess.py`).
- **Backend**: Flask API that loads the exported model, performs preprocessing identical to the notebook (resize to 224×224, normalize to `[0,1]`), produces class probabilities, and persists user-triggered results into PostgreSQL via SQLAlchemy.
- **Frontend**: React + Vite single-page app with upload workflow, preview, probability bar chart, and history view backed by Axios calls to the Flask API.
- **Database**: PostgreSQL `prediction_results` table tracking file path, predicted class, confidence, and timestamp. Managed via SQLAlchemy models and migration-ready schema file.
- **Deployment**: Docker images for backend and frontend, docker-compose wiring backend + PostgreSQL (frontend optional). Environment variables control model paths and DB connection strings for local/dev/prod environments (Docker, Railway, Render).

## Data & Modeling Flow
1. **Dataset Acquisition**: HAM10000 images + metadata downloaded via Kaggle CLI in Colab. Metadata CSV merged with image paths, missing metadata entries imputed with domain-aware defaults.
2. **Preprocessing**:
   - Metadata cleaning + label encoding (`lesion_id`, `dx`, `age`, `sex`, `localization`).
   - Image pipeline: resize to 224×224, convert to float32, normalize by `1/255`.
   - Imbalance mitigation through class weights (`sklearn`) and aggressive augmentation (`ImageDataGenerator` with rotations, zoom, hue shifts, etc.).
3. **Training & Evaluation**:
   - Transfer learning using EfficientNetB0 base + GAP + dropout + dense softmax head.
   - Callbacks: `EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`.
   - Metrics: accuracy, classification report, per-class recall, confusion matrix, ROC curves.
   - Artifacts saved to Google Drive and synced to repo's `model/artifacts/` folder for backend consumption.

## Backend Flow
1. **Upload** (`POST /predict`):
   - Accepts multipart image, stores sanitized copy to `UPLOAD_DIR`.
   - Preprocesses via shared `model/preprocessing.py` utilities.
   - Runs TensorFlow inference, returns predicted label, confidence, full probability vector, and saved image path.
2. **Persistence** (`POST /save-result`):
   - Receives JSON payload referencing prediction data and optional image path.
   - Inserts into PostgreSQL `prediction_results`.
3. **History** (`GET /history`):
   - Returns paginated or most-recent rows for frontend history page.

## Frontend Flow
- **Dashboard Page**: Drag-and-drop uploader with live preview, calls `/predict`, displays predicted class, confidence, probability chart, and allows saving results.
- **History Page**: Fetches `/history`, shows sortable table of prior predictions.
- **State Management**: React hooks; Axios for HTTP; environment-driven API base URL; Tailwind utility classes for styling.

## Deployment Strategy
- **Local**: `docker-compose up` to run Flask + PostgreSQL + optional frontend; or run services independently with `.env` files.
- **Production**: Container images built via provided Dockerfiles. Backend ready for Gunicorn + Flask in Render/Railway; frontend static build deployable to Netlify/Vercel. Model + label map mounted via volume or cloud storage.

This document guides subsequent implementation tasks and keeps deliverables aligned with project requirements.
