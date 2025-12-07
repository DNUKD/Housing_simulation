from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base
from datetime import datetime

# Simulation
class Simulation(Base):
    __tablename__ = "simulation"

    id = Column(Integer, primary_key=True, index=True)

    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)

    total_income = Column(Float, nullable=False)
    affordable_area = Column(Float, nullable=False)
    healthy_area = Column(Float, nullable=False)
    crowding_status = Column(String, nullable=False)
    created_at = Column(String, default=lambda: datetime.utcnow().isoformat())

    country = relationship("Country", back_populates="simulations")
    region = relationship("Region", back_populates="simulations")
    family_members = relationship("FamilyMember", back_populates="simulation")
