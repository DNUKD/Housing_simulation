from database.db import Base, engine
from database.seed_data import seed_all


# Initialize DB tables fill them with seed data
def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Load data from CSV
    seed_all()
