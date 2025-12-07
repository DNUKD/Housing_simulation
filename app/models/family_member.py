from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

# Family model
class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)

    simulation_id = Column(Integer, ForeignKey("simulation.id"), nullable=False)
    role = Column(String, nullable=False)

    simulation = relationship("Simulation", back_populates="family_members")
