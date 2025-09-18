from app.db.database import Base

from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String

from datetime import datetime


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.telegram_id"))
    site_id = Column(Integer, ForeignKey("sites.id"))
    status_code = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    error_message = Column(String, nullable=True)
    content_hash = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    site = relationship("Site", back_populates="logs")
    author = relationship("User", back_populates="logs")