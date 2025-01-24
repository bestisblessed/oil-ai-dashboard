import streamlit as st
import pandas as pd
import requests
import os

# Load environment variables
API_KEY = st.secrets["GRAPHHOPPER_API_KEY"]
st.title("Netback Calculator")
st.write("Calculate the netback for a single location and download report.")
tab1, tab2 = st.tabs(["Selling", "Buying"])
# Load cities from CSV
current_dir = os.path.dirname(__file__)
file_path = os.path.join(current_dir, "../data/all_cities.csv")
try:
    df = pd.read_csv(file_path)
    locations = [f"{city}, {country}" for city, country in zip(df['City'], df['Country'])]
    locations = sorted(set(locations))
except FileNotFoundError:
    st.error("Cities file not found. Using default cities list.")
    locations = ["New York, USA", "Los Angeles, USA", "London, UK", "Paris, France", "Tokyo, Japan"]
except Exception as e:
    st.error(f"Error loading cities: {str(e)}")
    locations = ["New York, USA", "Los Angeles, USA", "London, UK", "Paris, France", "Tokyo, Japan"]

# Initialize session state for distance calculation
if 'distance_calculated' not in st.session_state:
    st.session_state['distance_calculated'] = False

with tab1:
    st.subheader("Calculations")
    # location_name = st.text_input("Enter location name:", "Custom Location")
    

    # Set default indices for New York and Las Vegas
    try:
        default_start = locations.index("New York, United States")
        default_end = locations.index("Las Vegas, United States")
    except ValueError:
        default_start = 0
        default_end = 0

    # Dropdowns for selecting locations with defaults
    start_location = st.selectbox("Select starting location:", locations, index=default_start)
    end_location = st.selectbox("Select ending location:", locations, index=default_end)

    # Calculate Distance button
    distance_km = 0.0
    if st.button("Calculate Distance"):
        try:
            url = "https://nominatim.openstreetmap.org/search"
            headers = {'User-Agent': 'distance_calculator/1.0'}
            start_response = requests.get(url, params={"q": start_location, "format": "json", "limit": 1}, headers=headers)
            end_response = requests.get(url, params={"q": end_location, "format": "json", "limit": 1}, headers=headers)
            
            if start_response.ok and end_response.ok:
                start_data = start_response.json()[0]
                end_data = end_response.json()[0]
                
                route_url = "https://graphhopper.com/api/1/route"
                route_params = {
                    "point": [f"{start_data['lat']},{start_data['lon']}", f"{end_data['lat']},{end_data['lon']}"],
                    "profile": "car",
                    "locale": "en",
                    "calc_points": True,
                    "key": API_KEY
                }
                route_response = requests.get(route_url, params=route_params)
                
                if route_response.ok:
                    route = route_response.json()["paths"][0]
                    distance_km = route['distance'] / 1000
                    estimated_time_minutes = route['time'] / 60000

                    # Display the results in a similar format to calc_distance.py
                    st.write(f"\nRoute from {start_location} to {end_location}:")
                    st.write(f"**Distance:** {distance_km:.2f} km")
                    st.write(f"**Estimated Time:** {estimated_time_minutes:.2f} minutes")
                    st.write("-"*100)
                    # st.write("\nDirections:")
                    # for step in route["instructions"]:
                    #     st.write(f"{step['text']} ({step['distance']:.2f} meters)")

                    st.session_state['distance_calculated'] = True  # Set session state to True
                else:
                    st.error("Error calculating route")
            else:
                st.error("Error getting coordinates")
        except Exception as e:
            st.error(f"Error calculating distance: {str(e)}")

    # Sidebar input variables
    with st.sidebar:
        st.header("Constants")
        density_equalization_factor = 0.49
        sulphur_equalization_factor = 1.38
        st.write(f"Density Equalization Factor: {density_equalization_factor}")
        st.write(f"Sulphur Equalization Factor: {sulphur_equalization_factor}")
        st.header("Input Variables")
        delivered_density = st.number_input("Delivered Density", value=0.0)
        delivered_sulfur = st.number_input("Delivered Sulfur", value=0.0)
        conversion = st.number_input("Conversion Factor", value=0.0)
        wti = st.number_input("WTI", value=0.0)
        fx = st.number_input("FX Rate", value=0.0)
        diff = st.number_input("Differential", value=0.0)
        wadf = st.number_input("WADF", value=0.0)
        blending_uptick = st.number_input("Blending Uptick", value=0.0)
        pl_tariff = st.number_input("P/L Tariff", value=0.0)
        la = st.number_input("LA", value=0.0)
        dilutent_fee = st.number_input("Dilutent Fee", value=0.0)
        premium_or_discount = st.number_input("Premium or Discount", value=0.0)
        equalized = st.radio("Equalized?", ('Yes', 'No'), index=1)

    # Show Calculate Netback button only if distance is calculated
    if st.session_state['distance_calculated']:
    
                # Print all variable values after the distance calculation
        st.write(f"**Delivered Density:** {delivered_density}")
        st.write(f"**Delivered Sulfur:** {delivered_sulfur}")
        st.write(f"**Conversion Factor:** {conversion}")
        st.write(f"**WTI:** {wti}")
        st.write(f"**FX Rate:** {fx}")
        st.write(f"**Differential:** {diff}")
        st.write(f"**WADF:** {wadf}")
        st.write(f"**Blending Uptick:** {blending_uptick}")
        st.write(f"**P/L Tariff:** {pl_tariff}")
        st.write(f"**LA:** {la}")
        st.write(f"**Dilutent Fee:** {dilutent_fee}")
        st.write(f"**Premium or Discount:** {premium_or_discount}")
        st.write(f"**Equalized:** {'Yes' if equalized == 'Yes' else 'No'}")
        
        if st.button("Calculate Netback"):
            base_price = ((wti + diff) * conversion * fx) + wadf
            base_price_adjusted = base_price + blending_uptick
            sulfur_penalty = ((delivered_sulfur - 0.5) / 0.1) * sulphur_equalization_factor
            density_penalty = (delivered_density - 825) * density_equalization_factor
            eq = -(density_penalty + sulfur_penalty)
            trucking_charge = -(5.40 * distance_km) + 225
            netback = base_price_adjusted + eq + pl_tariff + trucking_charge + la + dilutent_fee + premium_or_discount

            st.success(f"Netback Calculated: {netback:.2f} USD")

            # Prepare a DataFrame for the result
            report_data = {
                "Location": [end_location],
                "Netback": [netback]
            }
            report_df = pd.DataFrame(report_data)

            @st.cache_data
            def convert_df(df):
                return df.to_csv(index=False).encode('utf-8')

            # Convert to CSV and provide download button
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

