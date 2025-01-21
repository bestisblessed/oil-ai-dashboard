import streamlit as st
from streamlit_folium import st_folium
import folium

def main():
    st.set_page_config(
        page_title="Oil AI - Your Oil and Gas Companion",
        page_icon="🚛",
        layout="wide",
    )
    st.title("Oil AI 🛢️")
    st.markdown("Intelligent Assistant for Oil and Gas Industry")
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

    # # Year Selection Section
    # st.markdown("## Select Years of Interest")
    # year_range = st.slider(
    #     "Select the range of years you are interested in:",
    #     min_value=1960,
    #     max_value=2022,
    #     value=(2000, 2020)
    # )
    # st.write(f"Selected years: {year_range[0]} to {year_range[1]}")
    # # Country Selection Section
    # st.markdown("## Select Regions or Countries")
    # countries = st.multiselect(
    #     "Which countries or regions would you like to analyze?",
    #     options=["USA", "Canada", "Saudi Arabia", "Russia", "Brazil", "Norway", "Nigeria", "China"],
    #     default=["USA", "Canada"]
    # )
    # st.write(f"Selected countries or regions: {', '.join(countries)}")

    st.header("Getting Started")

    # Oil Seller Location Selection Section
    st.markdown("#### Select Oil Seller Locations")
    seller_locations = st.multiselect(
        "Select the locations of oil sellers:",
        options=["Houston, USA", "Calgary, Canada", "Edmonton, Canada", "Dallas, USA", "Oklahoma City, USA", "Denver, USA", "Midland, USA", "Bakersfield, USA"],
        default=["Houston, USA"]
    )
    # st.write(f"Selected seller locations: {', '.join(seller_locations)}")


    # Interactive Map Section
    st.markdown("## Interactive Map of Oil Seller Locations")
    map_center = [40, -100]  # Center the map on North America
    folium_map = folium.Map(location=map_center, zoom_start=4)
    location_coordinates = {
        "Houston, USA": [29.7604, -95.3698],
        "Calgary, Canada": [51.0447, -114.0719],
        "Edmonton, Canada": [53.5333, -113.4938],
        "Dallas, USA": [32.7767, -96.7969],
        "Oklahoma City, USA": [35.4676, -97.5164],
        "Denver, USA": [39.7392, -104.9903],
        "Midland, USA": [31.9976, -102.0777],
        "Bakersfield, USA": [35.3733, -119.0187],
    }
    for location in seller_locations:
        if location in location_coordinates:
            folium.Marker(
                location=location_coordinates[location],
                popup=location,
                tooltip=location
            ).add_to(folium_map)
    st_folium(folium_map, width=700, height=500)



    # Oil Type Selection Section
    st.markdown("#### Select Oil Types for Analysis")
    oil_types = st.multiselect(
        "Choose the types of oil you want to analyze:",
        options=["Brent Crude", "WTI", "West Texas Intermediate (WTI)", "Dubai Crude", "Urals", "Bonny Light", "OPEC Basket", "Basrah Light"],
        default=["Brent Crude", "WTI"]
    )
    # st.write(f"Selected oil types: {', '.join(oil_types)}")

    # Equalized Input Section
    st.markdown("## Equalization Check")
    equalized = st.radio("Equalized? (y/n)", options=["Yes", "No"], index=1)
    # st.write(f"Equalized status: {equalized}")



    st.markdown("---")
    st.markdown(
        """
        Created by Tyler Durette
        OIL AI © 2025 | [GitHub](https://github.com/bestisblessed) | [Contact Me](mailto:tyler.durette@gmail.com)
        """
    )

if __name__ == "__main__":
    main()

