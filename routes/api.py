import requests

# Base URL of the backend API
BASE_URL = "http://127.0.0.1:8000"


def fetch_regions(country_id: int):
    """Fetch region list for a given country"""
    try:
        return requests.get(f"{BASE_URL}/regions/{country_id}").json()
    except Exception:
        return []


def run_simulation(payload: dict):
    """Submit input and return the response"""
    try:
        return requests.post(f"{BASE_URL}/simulation/", json=payload)
    except Exception:
        return None


def fetch_animated_values():
    """Fetch animated UI values """
    try:
        return requests.get(f"{BASE_URL}/animated_values").json()
    except Exception:
        return {}
