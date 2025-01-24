import streamlit as st
from streamlit_folium import st_folium
import folium

def main():
    st.set_page_config(
        page_title="Oil AI - Your Oil and Gas Companion",
        page_icon="🛢️",
        layout="wide",
    )

    # Sidebar
    # with st.sidebar:
        
        # st.header("Sidebar Options")
        
        # Navigation Menu
        # st.subheader("Navigation")
        # nav_option = st.radio("Go to:", options=["Home", "01_Chatbot_🤖", "02_Report_Generator_📄"])
        # st.write(f"Selected: {nav_option}")
        
        # Filters
        # st.subheader("Filters")
        # filter_year = st.slider("Year Filter:", min_value=1960, max_value=2022, value=(2000, 2020))
        # st.write(f"Filter Years: {filter_year[0]} to {filter_year[1]}")

        # selected_regions = st.multiselect("Select Regions:", ["North America", "Middle East", "Europe", "Asia", "South America", "Africa"], default=["North America"])
        # st.write(f"Selected Regions: {', '.join(selected_regions)}")

        # User Preferences
        # st.subheader("User Preferences")
        # dark_mode = st.checkbox("Enable Dark Mode", value=False)
        # notifications = st.checkbox("Enable Notifications", value=True)
        # st.write(f"Dark Mode: {'On' if dark_mode else 'Off'}, Notifications: {'On' if notifications else 'Off'}")

        # # Contact and Info
        # st.sidebar.markdown("<div style='height: 600px;'></div>", unsafe_allow_html=True)  # Adjust height as needed
        # st.subheader("Contact & Info")
        # st.markdown(
        #     """
        #     - [Support](mailto:support@oilai.com)
        #     - [Documentation](https://oilai-docs.com)
        #     - [GitHub](https://github.com/bestisblessed)
        #     """
        # )

    # Title
    st.title("Oil AI 🛢️")
    st.markdown("Intelligent assistant for oil and gas Industry")
    st.divider()
    st.markdown("## Features")
    st.markdown(
        """
        - **Data Analysis**: Analyze your oil and gas data effortlessly.
        - **Report Generation**: Generate comprehensive reports with ease, tailored to your business needs.
        - **Market Trends**: Explore latest market trends in the oil and gas industry.
        """
    )
    # st.divider()

    # Getting Started Section
    # st.header("Getting Started")

    # # Year Selection Scroll Section
    # st.markdown("## Select Year Range")
    # year_range = st.slider(
    #     "Select the range of years for your analysis:",
    #     min_value=1960,
    #     max_value=2022,
    #     value=(2000, 2020),
    #     step=1
    # )
    # st.write(f"Year range selected: {year_range[0]} to {year_range[1]}")

    # # Oil Seller Location Selection Section
    # st.markdown("#### Select Oil Seller Locations")
    # seller_locations = st.multiselect(
    #     "Select the locations of oil sellers:",
    #     options=["Houston, USA", "Calgary, Canada", "Edmonton, Canada", "Dallas, USA", "Oklahoma City, USA", "Denver, USA", "Midland, USA", "Bakersfield, USA"],
    #     default=["Houston, USA"]
    # )
    # st.write(f"Selected seller locations: {', '.join(seller_locations)}")


    # # Interactive Map Section
    # st.markdown("## Interactive Map of Oil Seller Locations")
    # map_center = [40, -100]  # Center the map on North America
    # folium_map = folium.Map(location=map_center, zoom_start=4)
    # location_coordinates = {
    #     "Houston, USA": [29.7604, -95.3698],
    #     "Calgary, Canada": [51.0447, -114.0719],
    #     "Edmonton, Canada": [53.5333, -113.4938],
    #     "Dallas, USA": [32.7767, -96.7969],
    #     "Oklahoma City, USA": [35.4676, -97.5164],
    #     "Denver, USA": [39.7392, -104.9903],
    #     "Midland, USA": [31.9976, -102.0777],
    #     "Bakersfield, USA": [35.3733, -119.0187],
    # }
    # for location in seller_locations:
    #     if location in location_coordinates:
    #         folium.Marker(
    #             location=location_coordinates[location],
    #             popup=location,
    #             tooltip=location
    #         ).add_to(folium_map)
    # st_folium(folium_map, width=700, height=500)


    st.markdown("---")
    st.markdown(
        """
        Created by Tyler Durette
        Oil AI © 2025 | [GitHub](https://github.com/bestisblessed) | [Contact Me](mailto:tyler.durette@gmail.com)
        """
    )

if __name__ == "__main__":
    main()

