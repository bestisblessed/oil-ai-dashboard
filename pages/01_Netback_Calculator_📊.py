import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import plotly.express as px
st.title("Netback Calculator")
st.write("Calculate the netback for locations and download report.")
current_dir = os.path.dirname(__file__)  
file_path = os.path.join(current_dir, "../data/locations.csv")  
try:
    locations_df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("The location_values.csv file could not be found. Please ensure it exists in the ../data directory.")
    st.stop()
# Initialize session state for results
if 'netback_results' not in st.session_state:
    st.session_state['netback_results'] = []
tab1, tab2 = st.tabs(["Selling", "Buying"])
with tab1:
    st.write("")
    st.subheader("Calculations")
    location_names = locations_df["Location"].tolist()
    selected_locations = st.multiselect(
        "Select locations:",
        options=location_names,
        default=[]
    )
    map_center = [40.0, -95.0]
    folium_map = folium.Map(location=map_center, zoom_start=4)
    location_coordinates = {
        "Lycos Dulwich": [51.0, -114.0],
        "Marlin Youngstown": [51.2, -112.5],
        "Marlin Fosterton": [50.8, -111.5]
    }
    for location in selected_locations:
        if location in location_coordinates:
            folium.Marker(
                location=location_coordinates[location],
                popup=location,
                tooltip=location
            ).add_to(folium_map)
    st_folium(folium_map, width=1000, height=500)
    with st.sidebar:
        st.header("Constants")
        location_values = {
            loc: locations_df[locations_df["Location"] == loc].iloc[0].to_dict()
            for loc in locations_df["Location"]
        }
        if selected_locations:
            default_row = locations_df[locations_df["Location"] == selected_locations[0]].iloc[0]
        else:
            default_row = locations_df.iloc[0]
        density_equalization_factor = 0.49
        sulphur_equalization_factor = 1.38
        st.write(f"Density Equalization Factor: {density_equalization_factor}")
        st.write(f"Sulphur Equalization Factor: {sulphur_equalization_factor}")
    if st.button("Calculate Netbacks"):
        results = []
        for location in selected_locations:
            loc_values = location_values[location]
            selected_distance = loc_values["Distance"]
            base_price = ((loc_values["WTI"] + loc_values["Differential"]) * 
                         loc_values["Conversion Factor"] * loc_values["FX Rate"]) + loc_values["WADF"]
            base_price_adjusted = base_price + loc_values["Blending Uptick"]
            sulfur_penalty = ((loc_values["Delivered Sulfur"] - 0.5) / 0.1) * sulphur_equalization_factor
            if loc_values["Delivered Density"] < 800:
                density_penalty = (800 - loc_values["Delivered Density"]) * density_equalization_factor
            elif 800 <= loc_values["Delivered Density"] < 825:
                density_penalty = 0
            else:
                density_penalty = (loc_values["Delivered Density"] - 825) * density_equalization_factor
            eq = -(density_penalty + sulfur_penalty)
            trucking_charge = -(5.40 * selected_distance) + 225
            netback = base_price_adjusted + eq + loc_values["P/L Tariff"] + trucking_charge + loc_values["LA"] + loc_values["Dilutent Fee"] + loc_values["Premium"]
            results.append({
                "Location": location,
                "Netback (CAD/m3)": round(netback, 2)
            })
        st.session_state['netback_results'] = results
    if st.session_state['netback_results']:
        results_df = pd.DataFrame(st.session_state['netback_results'])
        st.write("Netback Results:")
        st.dataframe(results_df.style.format({
            "Netback (CAD/m3)": "{:.2f}"
        }))
        report_data = []
        for location in selected_locations:
            netback_value = next((item["Netback (CAD/m3)"] for item in st.session_state['netback_results'] if item["Location"] == location), None)
            if netback_value is not None:
                report_data.append({
                    "Location": location,
                    "Netback (CAD/m3)": round(netback_value, 2)
                })
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
        st.divider()
        st.subheader("Analysis")
        st.write("")
        if len(st.session_state['netback_results']) > 1:
            best_option = max(st.session_state['netback_results'], key=lambda x: x["Netback (CAD/m3)"])
            worst_option = min(st.session_state['netback_results'], key=lambda x: x["Netback (CAD/m3)"])
            avg_netback = sum(r["Netback (CAD/m3)"] for r in st.session_state['netback_results']) / len(st.session_state['netback_results'])
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Best Option", 
                         f"{best_option['Location']}", 
                         f"${best_option['Netback (CAD/m3)']:.2f}/m³")
            with col2:
                st.metric("Average Netback", 
                         f"${avg_netback:.2f}/m³")
            with col3:
                st.metric("Spread (Best to Worst)", 
                         f"${best_option['Netback (CAD/m3)'] - worst_option['Netback (CAD/m3)']:.2f}/m³")
            fig = px.bar(results_df, x="Location", y="Netback (CAD/m3)", 
                          title="Netback by Location", 
                          color="Location", 
                          barmode="group", 
                          category_orders={"Location": results_df["Location"].unique()})
            fig.update_xaxes(title_text='Location')
            fig.update_yaxes(title_text='Netback (CAD/m3)')
            st.plotly_chart(fig)
            # Box Plot: Distribution of Netbacks
            if len(st.session_state['netback_results']) > 1:
                fig_box = px.box(results_df, x="Netback (CAD/m3)", title="Netback Distribution Across Locations", points="all")
                fig_box.update_xaxes(title_text="Netback (CAD/m3)")
                fig_box.update_yaxes(title_text="")  # Optional, remove y-axis label for cleaner display
                st.plotly_chart(fig_box)
            else:
                st.info("Select multiple locations to see the netback distribution.")
            # Sort results by netback value
            sorted_results = sorted(st.session_state['netback_results'], key=lambda x: x["Netback (CAD/m3)"], reverse=True)
            # Create comparison text
            comparison_text = [
                f"1. **{best_option['Location']}** is the most profitable option with a netback of ${best_option['Netback (CAD/m3)']:.2f}/m³."
            ]
            # Add comparisons for each location relative to the best option
            for result in sorted_results[1:]:
                difference = best_option["Netback (CAD/m3)"] - result["Netback (CAD/m3)"]
                comparison_text.append(
                    f"- **{result['Location']}** yields ${result['Netback (CAD/m3)']:.2f}/m³ "
                    f"(${difference:.2f}/m³ less than the best option)"
                )
            best_route = results_df.loc[results_df["Netback (CAD/m3)"].idxmax()]
            st.write("### Recommendation")
            st.write(f"Based on the calculations, the location with the highest netback is **{best_route['Location']}** with a netback of **{best_route['Netback (CAD/m3)']} CAD/m3**.")
        else:
            st.info("Please select multiple locations to see comparison analysis.")
with tab2:
    st.subheader("Calculations")
    st.write("Content for buying calculations will go here.")
