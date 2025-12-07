from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

# Country model
class Country(Base):
    __tablename__ = "countries"

    id =       Column(Integer, primary_key=True, index=True)
    code =     Column(String, nullable=False, unique=True)
    name =     Column(String, nullable=False)

    regions = relationship("Region", back_populates="country")
    wage_stats = relationship("WageStats", back_populates="country")
    simulations = relationship("Simulation", back_populates="country")

