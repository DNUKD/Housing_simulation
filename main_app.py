import sys
import os

# Fix module paths for Streamlit Cloud
ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ROOT)
sys.path.append(os.path.join(ROOT, "app"))
sys.path.append(os.path.join(ROOT, "database"))

import streamlit as st
from resources.style import tooltip_css
from routes.api import (fetch_regions, run_simulation, fetch_animated_values)
from sections.sections import (render_housing_affordability, render_income, render_rent, render_floor_area,render_household_chart, render_market_price)
from streamlit_autorefresh import st_autorefresh

ROLE_OPTIONS = {
    "Employed Adult": "adult_worker",
    "Unemployed Adult": "adult_unemployed",
    "Child": "child",
    "Senior": "retired",
}

# Page setup
st.set_page_config(page_title="Housing Simulation", page_icon="🏙️", layout="wide")
st_autorefresh(interval=3000, key="anim-refresh")
st.markdown(tooltip_css(), unsafe_allow_html=True)

# Sidebar Inputs
st.sidebar.header("Family Setup")
country_names = {"Hungary": 1, "Germany": 2, "France": 3, "Netherlands": 4, "Norway": 5}

# Select country
country_name = st.sidebar.selectbox("Choose country", list(country_names.keys()))
country_id = country_names[country_name]

# Select region
region_types = {"Capital": "capital", "City": "city", "Countryside": "countryside"}
region_type = st.sidebar.selectbox("Choose region", list(region_types.keys()))
region_type_value = region_types[region_type]

# Load region
region_lookup = fetch_regions(country_id)

region_id = None
for r in region_lookup:
    if r["type"].strip().lower() == region_type_value.strip().lower():
        region_id = r["id"]
        break

if region_id is None:
    st.error("Region not found in database.")
    st.stop()

# Family
family_size = st.sidebar.slider("Size of the family", 1, 6, 2)
st.sidebar.subheader("Household")

family_roles = []
for i in range(family_size):
    label = st.sidebar.selectbox(f"Family member #{i + 1}",list(ROLE_OPTIONS.keys()),key=f"member_{i}")
    family_roles.append(ROLE_OPTIONS[label])

# Run simulation
if st.sidebar.button("Run simulation"):
    payload = {"country_id": country_id, "region_id": region_id, "family_roles": family_roles}

    response = run_simulation(payload)

    if response.status_code != 200:
        st.error(response.text)
        st.stop()

    st.session_state["data"] = response.json()

if "data" not in st.session_state:
    st.info("Run the simulation.")
    st.stop()

data = st.session_state["data"]
animated = fetch_animated_values()
currency = data.get("currency", "Ft")

# Main Layout
st.markdown('<div class="limited-width-container">', unsafe_allow_html=True)

# Upper cols
colA, colB, colC, colD = st.columns(4)

render_housing_affordability(colA, data, animated, currency)
render_income(colB, data, animated, currency)
render_rent(colC, data, animated, currency)
render_floor_area(colD, data, animated, currency)

st.markdown('</div>', unsafe_allow_html=True)

# Chart + Market Price section
st.markdown('<div class="limited-width-container">', unsafe_allow_html=True)

colChart, colE = st.columns([3, 1])

render_household_chart(colChart, data, currency)

# E) col
render_market_price(colE, region_lookup, data, currency)
