from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .database import Base, engine
from .routers import auth, predict, history, notifications, otp_auth
import os


Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkinVision AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_dir = os.environ.get("STATIC_DIR", os.path.join(os.path.dirname(__file__), "static"))
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.include_router(auth.router, prefix="/auth", tags=["auth"])  # optional
app.include_router(predict.router, tags=["predict"])            # /predict
app.include_router(history.router, prefix="/history", tags=["history"])  # /history
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])  # /notifications
app.include_router(otp_auth.router, prefix="/otp", tags=["otp"])  # /otp


@app.get("/")
def root():
    return {"message": "SkinVision AI API is running"}


