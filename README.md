# SkinVision AI – Production Skin Cancer Detection System

A full-stack reference implementation for skin cancer classification built on the HAM10000 dataset. The project ships with:

- **Model pipeline** – Google Colab notebook for training EfficientNetB0 with class weights and heavy augmentation, plus exported artifacts (`model.h5`, `label_map.json`, `preprocessing.py`).
- **Backend API** – Flask + TensorFlow inference service with `/predict`, `/save-result`, and `/history` endpoints backed by PostgreSQL.
- **Frontend** – React + Vite dashboard that uploads images, visualizes probabilities, and displays persisted history.
- **DevOps** – Dockerfiles, docker-compose, OpenAPI contract, and deployment guidance for local, Docker, and managed hosts (Railway/Render + Netlify/Vercel).

> ⚠️ **Medical disclaimer:** This software is for research & education only. It is **not** a medical device and must not be used for clinical diagnosis.

---

## 1. Repository Layout

```
model/
  ├── artifacts/model.h5              # Placeholder EfficientNet weights (replace with trained model)
  ├── HAM10000_Training_Pipeline.ipynb # End-to-end Colab notebook
  ├── label_map.json                   # Class↔index mapping
  └── preprocessing.py                 # Shared preprocessing utilities
backend/
  ├── flask_app/                       # Flask application factory, routes, services, DB models
  ├── db/schema.sql                    # PostgreSQL table definition
  ├── openapi.yaml                     # REST contract (OpenAPI 3.0)
  ├── requirements.txt                 # Backend dependencies
  ├── Dockerfile                       # Production container (Gunicorn)
  └── wsgi.py                          # Entrypoint
frontend/
  ├── src/                             # React pages & components
  ├── package.json / vite.config.js    # Build tooling
  └── Dockerfile                       # Static build container
uploads/                                # Server-side image cache (gitignored)
docker-compose.yml                      # Backend + DB + optional frontend stack
README.md                               # You are here
```

Additional documentation:
- `docs/ARCHITECTURE.md` – system overview & data flow.
- `backend/openapi.yaml` – consumable REST specification.

---

## 2. Quick Start

### 2.1 Prerequisites

| Component  | Minimum Version | Notes                           |
|------------|-----------------|---------------------------------|
| Python     | 3.11            | Backend / tooling               |
| Node.js    | 20              | Frontend build                  |
| Docker     | 24+             | Optional but recommended        |
| PostgreSQL | 15 (Docker)     | Managed automatically via compose |

TensorFlow 2.17.1 (CPU) is installed via backend requirements for inference.

### 2.2 Run Everything with Docker

```bash
docker compose up --build
```

Services:
- Backend API: http://localhost:5000
- Frontend SPA: http://localhost:3000
- PostgreSQL: localhost:5432 (user/password `postgres` / `postgres`)

The backend container mounts `./model` (artifacts) and `./uploads` (prediction cache). Stop the stack with `docker compose down`.

### 2.3 Manual Local Setup

1. **Model artifacts** – ensure `model/artifacts/model.h5` and `model/label_map.json` exist. Replace the placeholder model with your trained weights when ready.
2. **Backend**
   ```bash
   cd backend
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   export DATABASE_URL="postgresql+psycopg2://postgres:postgres@localhost:5432/skinvision"
   export MODEL_PATH="$(pwd)/../model/artifacts/model.h5"
   export LABEL_MAP_PATH="$(pwd)/../model/label_map.json"
   export UPLOAD_DIR="$(pwd)/../uploads"
   python wsgi.py
   ```
3. **Frontend**
   ```bash
   cd frontend
   npm install
   echo "VITE_API_BASE=http://localhost:5000" > .env.local
   npm run dev
   ```
4. **Database** – start a local Postgres instance (or use Docker `postgres:15`) and run `backend/db/schema.sql` once to create `prediction_results`.

---

## 3. Model Training Pipeline (HAM10000)

- Notebook: `model/HAM10000_Training_Pipeline.ipynb` (designed for Google Colab).
- Highlights:
  - Kaggle download of HAM10000 metadata + images.
  - Missing value handling (`age`, `sex`, `localization`, `dx_type`).
  - Aggressive `ImageDataGenerator` augmentation + class weighting to combat imbalance.
  - EfficientNetB0 transfer learning (`GlobalAveragePooling → Dropout → Dense softmax`).
  - Callbacks: `EarlyStopping`, `ReduceLROnPlateau`, `ModelCheckpoint`.
  - Metrics: accuracy, confusion matrix, per-class recall, ROC curves.
  - Artifact export: `ham10000_effnetb0.h5`, `label_map.json`, `preprocessing.py` (identical logic to `model/preprocessing.py`).

When you finish training, copy the exported artifacts into `model/artifacts/` and redeploy the backend.

---

## 4. Backend API (Flask + TensorFlow)

### 4.1 Key Modules

- `flask_app/config.py` – central Settings (env vars, paths, upload dir management).
- `flask_app/services/inference.py` – singleton TensorFlow model loader + prediction logic.
- `flask_app/services/storage.py` – file-system helper for persisted uploads.
- `flask_app/routes/*` – `/predict`, `/save-result`, `/history`, `/health` endpoints.
- `flask_app/models.py` – SQLAlchemy model for `prediction_results`.

### 4.2 Environment Variables

| Variable        | Default (dev)                                       | Description                          |
|-----------------|-----------------------------------------------------|--------------------------------------|
| `DATABASE_URL`  | `postgresql+psycopg2://postgres:postgres@localhost:5432/skinvision` | SQLAlchemy connection URI           |
| `MODEL_PATH`    | `<repo_root>/model/artifacts/model.h5`              | TensorFlow `.h5` file                |
| `LABEL_MAP_PATH`| `<repo_root>/model/label_map.json`                  | JSON label map                       |
| `UPLOAD_DIR`    | `<repo_root>/uploads`                               | Where incoming images are stored     |
| `CORS_ORIGINS`  | `*`                                                 | Allowed origins for the SPA          |

### 4.3 REST Endpoints

See `backend/openapi.yaml` for a consumable contract.

| Endpoint        | Method | Description                              |
|-----------------|--------|------------------------------------------|
| `/health`       | GET    | Liveness probe                           |
| `/predict`      | POST   | Multipart image upload → prediction JSON |
| `/save-result`  | POST   | Persist prediction metadata to Postgres  |
| `/history`      | GET    | Paginated list of saved predictions      |

Example response (`POST /predict`):
```json
{
  "predicted_class": "mel",
  "confidence": 0.87,
  "image_path": "/app/uploads/20241210_ab12cd.png",
  "probabilities": [
    {"label": "mel", "score": 0.87},
    {"label": "bcc", "score": 0.05},
    {"label": "nv", "score": 0.04}
  ]
}
```

### 4.4 Database Schema

```sql
CREATE TABLE IF NOT EXISTS prediction_results (
    id SERIAL PRIMARY KEY,
    image_path TEXT,
    predicted_class TEXT NOT NULL,
    confidence REAL NOT NULL,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

Run `psql -f backend/db/schema.sql` once after provisioning PostgreSQL.

---

## 5. Frontend (React + Vite)

Features:
- Drag-and-drop uploader with preview.
- Probability bar chart + confidence summary.
- "Save Result" workflow that posts to `/save-result`.
- History page that queries `/history` and renders a table.

Key files:
- `src/pages/Dashboard.jsx` – upload & inference UI.
- `src/pages/History.jsx` – persisted results table.
- `src/components/ProbabilityChart.jsx`, `PredictionSummary.jsx`, `HistoryTable.jsx` – reusable widgets.
- `src/utils/api.js` – Axios client for backend endpoints.

Environment variable: `VITE_API_BASE` (defaults to `http://localhost:5000`). Set it to your deployed backend URL for production.

Build commands:
```bash
cd frontend
npm run dev       # local development
npm run build     # production bundle → dist/
```

---

## 6. Deployment Guide

### 6.1 Backend (Railway / Render)
1. Push the repo to GitHub.
2. Create a PostgreSQL add-on (or point to an external instance).
3. Configure environment variables (`DATABASE_URL`, `MODEL_PATH=/app/model/artifacts/model.h5`, `LABEL_MAP_PATH=/app/model/label_map.json`, `UPLOAD_DIR=/app/uploads`).
4. During build, copy your trained artifacts into the image (or mount object storage). For Render, add a build command such as `pip install -r backend/requirements.txt` and a start command `cd backend && gunicorn wsgi:app --bind 0.0.0.0:$PORT`.
5. Upload/attach the `model/` directory (Render: use persistent disk or deploy hook; Railway: add a volume and copy artifacts at deploy time).

### 6.2 Frontend (Netlify / Vercel)
1. Set `VITE_API_BASE=https://<your-backend-domain>`.
2. Build command `npm run build`, output directory `dist`.
3. Ensure CORS on the backend allows the deployed origin (set `CORS_ORIGINS`).

### 6.3 Docker / Kubernetes
- Use `docker-compose.yml` for local dev or single-node deployments.
- For Kubernetes, build the backend and frontend images separately from their Dockerfiles and mount secrets/config maps for environment variables plus a persistent volume for `/app/uploads`.

---

## 7. Testing & Verification

- **Backend smoke test**: `curl -f http://localhost:5000/health` once the service is up.
- **Database**: Insert a manual record with `INSERT INTO prediction_results ...` and confirm `/history` returns it.
- **Frontend**: `npm run test` (Vitest) if you want to adapt/extend the existing suite.

> TensorFlow-heavy unit tests are not bundled to keep CI light; integration testing happens via manual workflows or lightweight API checks.

---

## 8. How to Use the System

1. **Train (optional)** – Run the Colab notebook, export `model.h5`, `label_map.json`, and `preprocessing.py`, then update `model/artifacts/`.
2. **Start services** – either via Docker or manual steps above.
3. **Upload** – Visit `http://localhost:3000`, drop a HAM10000-style dermatoscopic image, click **Predict**.
4. **Review** – Confidence + probability chart render instantly; click **Save Result** to persist to PostgreSQL.
5. **History** – Switch to the History tab to audit all saved predictions.

---

## 9. Reference Files

- **Training**: `model/HAM10000_Training_Pipeline.ipynb`
- **Preprocessing utilities**: `model/preprocessing.py`
- **REST contract**: `backend/openapi.yaml`
- **Architecture**: `docs/ARCHITECTURE.md`

Feel free to extend the system with Grad-CAM visualizations, authentication, analytics dashboards, or production observability as needed.

---

## 10. Support & Contributions

Issues and enhancements are welcome via GitHub pull requests. Please include:
- Description of the change / bug.
- Steps to reproduce (if relevant).
- Screenshots or logs when touching UX or infrastructure pieces.

Happy building! 🎯
