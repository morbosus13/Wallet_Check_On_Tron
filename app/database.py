from sqlalchemy import StaticPool, create_engine

from app.models import Base

DB_URL = "sqlite:///"
engine = create_engine(
    url=DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

Base.metadata.create_all(engine)
