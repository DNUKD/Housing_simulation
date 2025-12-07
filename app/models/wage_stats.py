from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

# Stats
class WageStats(Base):
    __tablename__ = "wage_stats"

    id = Column(Integer, primary_key=True, index=True)
    country_id = Column(Integer, ForeignKey("countries.id"), nullable=False)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)

    # adult_worker / adult_unemployed / retired / child
    role = Column(String, nullable=False)
    median_income = Column(Float, nullable=False)

    country = relationship("Country", back_populates="wage_stats")
    region = relationship("Region", back_populates="wage_stats")
