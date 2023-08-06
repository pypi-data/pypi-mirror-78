from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

__all__ = [
    "Base",
    "engine",
    "session_factory",
    "db_session"
]


DATABASE_CONNECTION_STRING = 'mysql+pymysql://test:test-321@localhost:3306/fi'

Base = declarative_base()
engine = create_engine(DATABASE_CONNECTION_STRING)
session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
db_session = scoped_session(session_factory)
Base.query_property = db_session.query_property()
