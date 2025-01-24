import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.title("Netback Calculator")
st.write("Calculate the netback for a single location and download report.")
# st.divider()

# Create tabs
tab1, tab2 = st.tabs(["Selling", "Buying"])

with tab1:
    # Current Netback Calculator content for Selling
    st.subheader("Calculations")
    locations = {
        "Lycos Dulwich": 42.59,
        "Marlin Youngstown": 51.94,
        "Marlin Fosterton": 55.74
    }
    seller_location = st.selectbox(
        "Select location:",
        options=["Lycos Dulwich", "Marlin Youngstown", "Marlin Fosterton"],
        index=0
    )

    selected_distance = locations[seller_location]
    st.write(f"Distance for {seller_location}: {selected_distance:.2f} km")

    # Interactive Map Section
    # st.markdown("## Interactive Map of Oil Seller Locations")
    map_center = [40.0, -95.0]  # Shift the map center a little north
    folium_map = folium.Map(location=map_center, zoom_start=4)  # Adjusted zoom level
    location_coordinates = {
        "Lycos Dulwich": [51.0, -114.0],
        "Marlin Youngstown": [51.2, -112.5],
        "Marlin Fosterton": [50.8, -111.5]
    }

    if seller_location in location_coordinates:
        folium.Marker(
            location=location_coordinates[seller_location],
            popup=seller_location,
            tooltip=seller_location
        ).add_to(folium_map)
    st_folium(folium_map, width=1000, height=500)

    with st.sidebar:
        st.header("Input Variables")
        
        # Initialize variables
        if seller_location == "Lycos Dulwich":
            wti = 67.9
            diff = -11.4
            conversion = 6.28981
            fx = 1.399
            wadf = 0
            blending_uptick = 0
            pl_tariff = -7.83
            la = 0
            delivered_density = 936.9
            delivered_sulfur = 3.31
            # distance = 42.59
        elif seller_location == "Marlin Youngstown":
            wti = 67.9
            diff = -6
            conversion = 6.29287
            fx = 1.399
            wadf = 0
            blending_uptick = 18
            pl_tariff = -26.25
            la = 0
            delivered_density = 967.7
            delivered_sulfur = 3.6
            # distance = 51.94
        else:  # For Marlin Fosterton
            wti = 0
            diff = 0
            conversion = 0
            fx = 0
            wadf = 0
            blending_uptick = 0
            pl_tariff = 0
            la = 0
            delivered_density = 0
            delivered_sulfur = 0
            # distance = 0

        # Display input fields
        delivered_density = st.text_input("Delivered Density", value=delivered_density)
        delivered_sulfur = st.text_input("Delivered Sulfur", value=delivered_sulfur)
        conversion = st.text_input("Conversion Factor", value=conversion)
        wti = st.text_input("WTI", value=wti)
        fx = st.text_input("FX Rate", value=fx)
        diff = st.text_input("Differential", value=diff)
        wadf = st.text_input("WADF", value=wadf)
        blending_uptick = st.text_input("Blending Uptick", value=blending_uptick)
        pl_tariff = st.text_input("P/L Tariff", value=pl_tariff)
        la = st.text_input("LA", value=la)
        # distance = st.text_input("Distance", value=distance)

        st.header("Constants")
        density_equalization_factor = 0.49
        sulphur_equalization_factor = 1.38
        st.write(f"Density Equalization Factor: {density_equalization_factor}")
        st.write(f"Sulphur Equalization Factor: {sulphur_equalization_factor}")


    if st.button("Calculate Netback"):
        # Convert inputs to floats
        wti = float(wti)
        diff = float(diff)
        conversion = float(conversion)
        fx = float(fx)
        wadf = float(wadf)
        blending_uptick = float(blending_uptick)
        pl_tariff = float(pl_tariff)
        la = float(la)
        delivered_density = float(delivered_density)
        delivered_sulfur = float(delivered_sulfur)

        base_price = ((wti + diff) * conversion * fx) + wadf
        base_price_adjusted = base_price + blending_uptick
        sulfur_penalty = ((delivered_sulfur - 0.5) / 0.1) * sulphur_equalization_factor
        density_penalty = (delivered_density - 825) * density_equalization_factor
        eq = -(density_penalty + sulfur_penalty)
        trucking_charge = -(5.40 * selected_distance) + 225
        netback = base_price_adjusted + eq + pl_tariff + trucking_charge + la

        st.success(f"Netback Calculated: {netback:.9f} USD")

        # Generate downloadable report
        report_data = {
            "Variable": [
                "WTI", "Differential", "Conversion Factor", "FX Rate", "WADF", "Blending Uptick", "Pipeline Tariff", "Trucking Charge", "LA", "Delivered Density", "Delivered Sulfur", "Distance", "Sulphur Equalization Factor", "Density Equalization Factor", "Netback"
            ],
            "Value": [
                wti, diff, conversion, fx, wadf, blending_uptick, pl_tariff, trucking_charge, la, delivered_density, delivered_sulfur, selected_distance, sulphur_equalization_factor, density_equalization_factor, netback
            ]
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
    # Buying tab content
    st.subheader("Calculations")
    st.write("Content for buying calculations will go here.")
    # Add your buying-specific content here
