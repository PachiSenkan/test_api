from sqlalchemy import Column, String, Float, Integer

from app.core.db import Base


class DDoSInformation(Base):
    __tablename__ = "attacks"

    id = Column(Integer, primary_key=True)
    source_address = Column(String, unique=True, index=True)
    average_duration = Column(Float)
