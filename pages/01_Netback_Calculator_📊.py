import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import plotly.express as px
from io import BytesIO
st.title("Netback Calculator")
st.write("Calculate the netback for locations and download report.")
current_dir = os.path.dirname(__file__)  
file_path = os.path.join(current_dir, "../data/locations.csv")  
try:
    locations_df = pd.read_csv(file_path)
except FileNotFoundError:
    st.error("The location_values.csv file could not be found. Please ensure it exists in the ../data directory.")
    st.stop()
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
                "Netback (CAD/m³)": round(netback, 2)
            })
        st.session_state['netback_results'] = results
    if st.session_state['netback_results']:
        results_df = pd.DataFrame(st.session_state['netback_results'])
        st.write("Netback Results:")
        st.dataframe(results_df.style.format({
            "Netback (CAD/m³)": "{:.2f}"
        }))
        def generate_html_report(df, bar_chart, box_plot, best_route):
            html_content = f"""
            <html>
            <head>
                <title>Netback Report</title>
            </head>
            <body>
                <h1 style="text-align: center;">Netback Report</h1>
                <h2>Results Table</h2>
                {df.to_html(index=False)}
                <h2>Recommendation</h2>
                <p>Based on the calculations, the location with the highest netback is <strong>{best_route['Location']}</strong> with a netback of <strong>{best_route['Netback (CAD/m³)']}</strong> CAD/m³.</p>
                <h2>Netback by Location</h2>
                {bar_chart.to_html(full_html=False, include_plotlyjs='cdn')}
                <h2>Netback Distribution</h2>
                {box_plot.to_html(full_html=False, include_plotlyjs='cdn')}
            </body>
            </html>
            """
            return html_content
        fig_bar = px.bar(results_df, x="Location", y="Netback (CAD/m³)", title="Netback by Location", color="Location")
        fig_box = px.box(results_df, x="Netback (CAD/m³)", title="Netback Distribution Across Locations", points="all")
        best_route = results_df.loc[results_df["Netback (CAD/m³)"].idxmax()]
        html_report = generate_html_report(results_df, fig_bar, fig_box, best_route)
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="netback_results.csv",
            mime="text/csv"
        )
        st.download_button(
            label="Download Report as HTML",
            data=html_report.encode('utf-8'),
            file_name="netback_report.html",
            mime="text/html"
        )
        st.divider()
        st.subheader("Analysis")
        st.write("")
        if len(st.session_state['netback_results']) > 1:
            best_option = max(st.session_state['netback_results'], key=lambda x: x["Netback (CAD/m³)"])
            worst_option = min(st.session_state['netback_results'], key=lambda x: x["Netback (CAD/m³)"])
            avg_netback = sum(r["Netback (CAD/m³)"] for r in st.session_state['netback_results']) / len(st.session_state['netback_results'])
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Best Option", 
                         f"{best_option['Location']}", 
                         f"${best_option['Netback (CAD/m³)']:.2f}/m³")
            with col2:
                st.metric("Average Netback", 
                         f"${avg_netback:.2f}/m³")
            with col3:
                st.metric("Spread (Best to Worst)", 
                         f"${best_option['Netback (CAD/m³)'] - worst_option['Netback (CAD/m³)']:.2f}/m³")
            st.plotly_chart(fig_bar)
            st.plotly_chart(fig_box)
        else:
            st.info("Please select multiple locations to see comparison analysis.")
        best_route = results_df.loc[results_df["Netback (CAD/m³)"].idxmax()]
        st.write("### Recommendation")
        st.write(f"Based on the calculations, the location with the highest netback is **{best_route['Location']}** with a netback of **{best_route['Netback (CAD/m³)']} CAD/m³**.")
with tab2:
    st.subheader("Calculations")
    st.write("Content for buying calculations will go here.")
