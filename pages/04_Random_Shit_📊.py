import streamlit as st
import pandas as pd

st.title("Expanding Capabilities")
st.divider()

st.markdown("#### Select Oil Type:")
oil_types = st.multiselect(
    "Choose the types of oil you want to analyze:",
    options=["Brent Crude", "WTI", "West Texas Intermediate (WTI)", "Dubai Crude", "Urals", "Bonny Light", "OPEC Basket", "Basrah Light"],
    default=["Brent Crude", "WTI"]
)
st.divider()
