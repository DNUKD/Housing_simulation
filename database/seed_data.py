import csv
from database.db import SessionLocal
from app.models.country import Country
from app.models.region import Region
from app.models.wage_stats import WageStats

DATA_DIR = "data/"


def load_csv(filename: str):
    with open(DATA_DIR + filename, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def seed_countries(db):
    rows = load_csv("countries.csv")
    if db.query(Country).first():
        return

    for row in rows:
        db.add(Country(
            id=int(row["id"]),
            code=row["code"],
            name=row["name"]
        ))
    db.commit()


def seed_regions(db):
    rows = load_csv("regions.csv")
    if db.query(Region).first():
        return

    for row in rows:
        db.add(Region(
            id=int(row["id"]),
            country_id=int(row["country_id"]),
            type=row["type"],
            wage_multiplier=float(row["wage_multiplier"]),
            rent_persqm=float(row["rent_persqm"])
        ))
    db.commit()


def seed_wage_stats(db):
    rows = load_csv("wage_stats.csv")
    if db.query(WageStats).first():
        return

    for row in rows:
        db.add(WageStats(
            id=int(row["id"]),
            country_id=int(row["country_id"]),
            region_id=int(row["region_id"]),
            role=row["role"],
            median_income=float(row["median_income"])
        ))
    db.commit()


# Runs all seeders
def seed_all():
    db = SessionLocal()
    seed_countries(db)
    seed_regions(db)
    seed_wage_stats(db)
    db.close()
