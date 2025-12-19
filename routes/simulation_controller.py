from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import SessionLocal
from pydantic import BaseModel

from app.services.simulation_service import run_simulation_logic

# Url map for sim, tells FastAPI to what func belongs to it
router = APIRouter(prefix="/simulation", tags=["simulation"])

# Scoped DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Expected input structure for starting (Pydantic model) json-obj
class SimulationInput(BaseModel):
    country_id: int
    region_id: int
    family_roles: list


# endpoint, if a post request & in the router prefix - then call this
@router.post("/")
def run_simulation  (
        data: SimulationInput,
        db: Session = Depends(get_db)
):
    return run_simulation_logic(
        data.country_id,
        data.region_id,
        data.family_roles,
        db
    )

