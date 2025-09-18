from app.db.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer



class User(Base):
    __tablename__ = "users"
    telegram_id = Column(Integer, primary_key=True, index=True, unique=True)

    sites = relationship("Site", back_populates="owner", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="author", cascade="all, delete-orphan")