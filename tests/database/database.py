from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite:///./testapp.db",
    connect_args={"check_same_thread": False},
)

TestSessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
