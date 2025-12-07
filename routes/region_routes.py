from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db import SessionLocal
from app.models.region import Region

# Region-related endpoints
router = APIRouter(prefix="/regions", tags=["regions"])

# DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Returns regions belonging to a given country
@router.get("/{country_id}")
def list_regions(country_id: int, db: Session = Depends(get_db)):
    rows = db.query(Region).filter(Region.country_id == country_id).all()

    return [
        {
            "id": r.id,
            "type": r.type,
            "wage_multiplier": r.wage_multiplier,
            "rent_persqm": r.rent_persqm,
        }
        for r in rows
    ]
