from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base




class Item(Base):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    Latitude = Column(Integer)
    Longitude = Column(Integer)
