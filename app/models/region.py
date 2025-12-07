from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

# Region with wage and rent
class Region(Base):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)

    type = Column(String, nullable=False)  # capital / city / countryside
    wage_multiplier = Column(Float, nullable=False)
    rent_persqm= Column(Float, nullable=False)

    country = relationship("Country", back_populates="regions")
    wage_stats = relationship("WageStats", back_populates="region")
    simulations = relationship("Simulation", back_populates="region")
