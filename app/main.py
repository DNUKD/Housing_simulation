import sys
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from fastapi import FastAPI
from database.init_db import init_db
from routes.simulation_controller import router as simulation_router
from routes.region_routes import router as region_router
from app.services.animation_service import (start_animation_thread,get_animated_values)

app = FastAPI()

# Create DB tables, load CSV data
init_db()

# Register API routes
app.include_router(region_router)
app.include_router(simulation_router)

# Endpoint returning anim val
@app.get("/animated_values")
def animated_values():
    return get_animated_values()

# Start background anim worker on startup
@app.on_event("startup")
def start_worker():
    start_animation_thread()
