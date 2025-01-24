import streamlit as st
from streamlit_folium import st_folium
import folium
st.set_page_config(
    page_title="Oil AI - Your Oil and Gas Companion",
    page_icon="🛢️",
    layout="wide",
)
st.title("Oil AI 🛢️")
st.markdown("Intelligent assistant for oil and gas industry")
st.divider()
st.markdown("## Features")
st.markdown(
    """
    - **Data Analysis**: Analyze your oil and gas data effortlessly.
    - **Report Generation**: Generate comprehensive reports with ease, tailored to your business needs.
    - **Market Trends**: Explore latest market trends in the oil and gas industry.
    """
)
st.divider()
st.header("Formulas")
st.write("")
st.markdown("##### **Base Price**")
st.code("Base Price = (( WTI + Diff ) x Conversion x FX ) + WADF")
st.write("")
st.markdown("##### **Base Price Adjusted**")
st.code("Base Price Adjusted = Base Price + Blending Uptick")
st.write("")
st.markdown("##### **Trucking Charge**")
st.code("Trucking Charge = ( 5.40 x Distance ) + 225")
st.write("")
st.markdown("##### **Density Penalty**")
st.code("""
If Delivered Density < 800: 
    Density Penalty = (800 - Delivered Density) * Density Equalization Factor
If Delivered Density >= 800 and Delivered Density < 825:
    Density Penalty = 0
If Delivered Density >= 825:
    Density Penalty = (Delivered Density - 825) * Density Equalization Factor
""")
st.write("")
st.markdown("##### **Sulphur Penalty**")
st.code("Sulphur Penalty = ((delivered_sulfur - 0.5) / 0.1) x sulphur_equalization_factor")
st.write("")
st.markdown("##### **EQ**")
st.code("EQ = -(Density Penalty + Sulphur Penalty)")
st.write("")
st.markdown("##### **Netback**")
st.code("Netback = Base Price Adjusted + EQ + P/L Tariff + Trucking Charge + LA + Dilutent Fee + Premium")
st.write("")
st.markdown("---")
st.markdown(
    """
    Created by Tyler Durette | Oil AI © 2025 | [GitHub](https://github.com/bestisblessed) | [Contact Me](mailto:tyler.durette@gmail.com)
    """
)
