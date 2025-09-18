from app.db.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey, String


class Site(Base):
    __tablename__ = "sites"
    id = Column(Integer, primary_key=True)
    telegram_id_author = Column(Integer, ForeignKey("users.telegram_id"))
    url = Column(String, nullable=False)
    check_interval = Column(Integer, default=5)

    owner = relationship("User", back_populates="sites")
    logs = relationship("Log", back_populates="site", cascade="all, delete-orphan")