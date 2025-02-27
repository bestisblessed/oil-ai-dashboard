import streamlit as st
import pandas as pd
import requests
import os
API_KEY = st.secrets["GRAPHHOPPER_API_KEY"]
st.title("Netback Calculator")
st.write("Calculate the netback for a single location and download report.")
tab1, tab2 = st.tabs(["Selling", "Buying"])
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
if 'distance_calculated' not in st.session_state:
    st.session_state['distance_calculated'] = False
with tab1:
    st.subheader("Calculations")
    try:
        default_start = locations.index("New York, United States")
        default_end = locations.index("Las Vegas, United States")
    except ValueError:
        default_start = 0
        default_end = 0
    start_location = st.selectbox("Select starting location:", locations, index=default_start)
    end_location = st.selectbox("Select ending location:", locations, index=default_end)
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
                    st.write(f"\nRoute from {start_location} to {end_location}:")
                    st.write(f"**Distance:** {distance_km:.2f} km")
                    st.write(f"**Estimated Time:** {estimated_time_minutes:.2f} minutes")
                    st.write("-"*100)
                    st.session_state['distance_calculated'] = True  
                else:
                    st.error("Error calculating route")
            else:
                st.error("Error getting coordinates")
        except Exception as e:
            st.error(f"Error calculating distance: {str(e)}")
    with st.sidebar:
        st.header("Constants")
        density_equalization_factor = 0.49
        sulphur_equalization_factor = 1.38
        st.write(f"Density Equalization Factor: {density_equalization_factor}")
        st.write(f"Sulphur Equalization Factor: {sulphur_equalization_factor}")
        st.header("Input Variables")
        delivered_density = st.number_input("Delivered Density", value=None, format="%f")
        delivered_sulfur = st.number_input("Delivered Sulfur", value=None, format="%f")
        conversion = st.number_input("Conversion Factor", value=None, format="%f")
        wti = st.number_input("WTI", value=None, format="%f")
        fx = st.number_input("FX Rate", value=None, format="%f")
        diff = st.number_input("Differential", value=None, format="%f")
        wadf = st.number_input("WADF", value=None, format="%f")
        blending_uptick = st.number_input("Blending Uptick", value=None, format="%f")
        pl_tariff = st.number_input("P/L Tariff", value=None, format="%f")
        la = st.number_input("LA", value=None, format="%f")
        dilutent_fee = st.number_input("Dilutent Fee", value=None, format="%f")
        premium = st.number_input("Premium or Discount", value=None, format="%f")
        equalized = st.radio("Equalized?", ('Yes', 'No'), index=1)
    if st.session_state['distance_calculated']:
        delivered_density = delivered_density if delivered_density is not None else 0.0
        delivered_sulfur = delivered_sulfur if delivered_sulfur is not None else 0.0
        conversion = conversion if conversion is not None else 0.0
        wti = wti if wti is not None else 0.0
        fx = fx if fx is not None else 0.0
        diff = diff if diff is not None else 0.0
        wadf = wadf if wadf is not None else 0.0
        blending_uptick = blending_uptick if blending_uptick is not None else 0.0
        pl_tariff = pl_tariff if pl_tariff is not None else 0.0
        la = la if la is not None else 0.0
        dilutent_fee = dilutent_fee if dilutent_fee is not None else 0.0
        premium = premium if premium is not None else 0.0
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
        st.write(f"**Premium or Discount:** {premium}")
        st.write(f"**Equalized:** {'Yes' if equalized == 'Yes' else 'No'}")
        if st.button("Calculate Netback"):
            base_price = ((wti + diff) * conversion * fx) + wadf
            base_price_adjusted = base_price + blending_uptick
            if delivered_density < 800:
                density_penalty = (800 - delivered_density) * density_equalization_factor
            elif 800 <= delivered_density < 825:
                density_penalty = 0
            else:  
                density_penalty = (delivered_density - 825) * density_equalization_factor
            sulfur_penalty = ((delivered_sulfur - 0.5) / 0.1) * sulphur_equalization_factor
            eq = -(density_penalty + sulfur_penalty)
            trucking_charge = -(5.40 * distance_km) + 225
            netback = base_price_adjusted + eq + pl_tariff + trucking_charge + la + dilutent_fee + premium
            st.divider()
            st.success(f"Netback Calculated: {netback:.2f}")
            report_data = {
                "Location": [end_location],
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
