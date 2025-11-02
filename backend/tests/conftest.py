import os
import tempfile
import shutil
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db


@pytest.fixture(scope="session")
def test_engine():
    # Use a temporary file-based sqlite DB to persist across connections
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        engine.dispose()
        try:
            os.remove(db_path)
        except FileNotFoundError:
            pass


@pytest.fixture()
def db_session(test_engine):
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture()
def client(db_session):
    # Override FastAPI dependency to use test DB
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    # Use temp static directory per test to avoid polluting repo
    temp_static_dir = tempfile.mkdtemp(prefix="static_")
    old_static = os.environ.get("STATIC_DIR")
    os.environ["STATIC_DIR"] = temp_static_dir

    with TestClient(app) as c:
        try:
            yield c
        finally:
            # Cleanup
            app.dependency_overrides.clear()
            if old_static is None:
                os.environ.pop("STATIC_DIR", None)
            else:
                os.environ["STATIC_DIR"] = old_static
            shutil.rmtree(temp_static_dir, ignore_errors=True)


