import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, unique=True, nullable=False)

# Check for testing environment
if os.getenv("TESTING"):
    engine = create_engine("sqlite:///:memory:")  # Use in-memory database for testing
else:
    engine = create_engine("sqlite:///app.db")  # File-based database for production

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
