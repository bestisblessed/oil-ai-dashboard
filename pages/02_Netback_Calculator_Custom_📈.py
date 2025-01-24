import streamlit as st
import pandas as pd
st.title("Netback Calculator")
st.write("Calculate the netback for a single location and download report.")
tab1, tab2 = st.tabs(["Selling", "Buying"])
with tab1:
    st.subheader("Calculations")
    location_name = st.text_input("Enter location name:", "Custom Location")
    distance = st.number_input("Enter distance (km):", value=0.0, min_value=0.0)
    with st.sidebar:
        st.header("Input Variables")
        delivered_density = st.number_input("Delivered Density", value=0.0)
        delivered_sulfur = st.number_input("Delivered Sulfur", value=0.0)
        conversion = st.number_input("Conversion Factor", value=0.0)
        wti = st.number_input("WTI", value=0.0)
        fx = st.number_input("FX Rate", value=0.0)
        diff = st.number_input("Differential", value=0.0)
        wadf = st.number_input("WADF", value=0.0)
        blending_uptick = st.number_input("Blending Uptick", value=0.0)
        pl_tariff = st.number_input("Pipeline Tariff", value=0.0)
        la = st.number_input("LA", value=0.0)
        st.header("Constants")
        density_equalization_factor = 0.49
        sulphur_equalization_factor = 1.38
        st.write(f"Density Equalization Factor: {density_equalization_factor}")
        st.write(f"Sulphur Equalization Factor: {sulphur_equalization_factor}")
    if st.button("Calculate Netback"):
        base_price = ((wti + diff) * conversion * fx) + wadf
        base_price_adjusted = base_price + blending_uptick
        sulfur_penalty = ((delivered_sulfur - 0.5) / 0.1) * sulphur_equalization_factor
        density_penalty = (delivered_density - 825) * density_equalization_factor
        eq = -(density_penalty + sulfur_penalty)
        trucking_charge = -(5.40 * distance) + 225
        netback = base_price_adjusted + eq + pl_tariff + trucking_charge + la
        st.success(f"Netback Calculated: {netback:.2f} USD")
        report_data = {
            "Location": [location_name],
            "Netback": [netback]
        }
        report_df = pd.DataFrame(report_data)
        @st.cache_data
        def convert_df(df):
            return df.to_csv(index=False).encode('utf-8')
        csv = convert_df(report_df)
        st.download_button(
            label="Download Report as CSV",
            data=csv,
            file_name="netback_report.csv",
            mime="text/csv",
        )
with tab2:
    st.subheader("Calculations")
    st.write("Content for buying calculations will go here.")
