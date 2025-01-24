import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random  # For demo data

def calculate_total_cost(base_price, distance_factor, quality_factor):
    """Calculate total cost including transportation and quality adjustments"""
    return base_price * distance_factor * quality_factor

def generate_mock_data(seller_location, oil_type):
    """Generate realistic mock data for demonstration"""
    base_prices = {
        "Brent Crude": 85.50,
        "WTI": 82.30,
        "West Texas Intermediate (WTI)": 82.30,
        "Dubai Crude": 81.75,
        "Urals": 71.20,
        "Bonny Light": 84.90,
        "OPEC Basket": 83.45,
        "Basrah Light": 80.15
    }
    
    # Distance factors (closer locations have lower transportation costs)
    distance_factors = {
        "Houston, USA": 1.02,
        "Calgary, Canada": 1.08,
        "Edmonton, Canada": 1.09,
        "Dallas, USA": 1.03,
        "Oklahoma City, USA": 1.04,
        "Denver, USA": 1.06,
        "Midland, USA": 1.05,
        "Bakersfield, USA": 1.07
    }
    
    base_price = base_prices.get(oil_type, 80.0)
    distance_factor = distance_factors.get(seller_location, 1.05)
    quality_factor = random.uniform(0.98, 1.02)  # Random quality variation
    
    return base_price, distance_factor, quality_factor

def main():
    st.set_page_config(page_title="Oil AI - Report Generator", page_icon="📄", layout="wide")
    
    st.title("Oil Cost Analysis Report 📄")
    st.markdown("Generate comprehensive cost analysis reports for different oil sellers")
    st.divider()

    # Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        seller_locations = st.multiselect(
            "Select Oil Seller Locations to Compare:",
            options=["Houston, USA", "Calgary, Canada", "Edmonton, Canada", 
                    "Dallas, USA", "Oklahoma City, USA", "Denver, USA", 
                    "Midland, USA", "Bakersfield, USA"],
            default=["Houston, USA", "Calgary, Canada"]
        )

    with col2:
        oil_type = st.selectbox(
            "Select Oil Type:",
            options=["Brent Crude", "WTI", "Dubai Crude", "Urals", 
                    "Bonny Light", "OPEC Basket", "Basrah Light"]
        )

    if st.button("Generate Report"):
        if not seller_locations:
            st.warning("Please select at least one seller location.")
            return

        # Generate comparison data
        comparison_data = []
        for location in seller_locations:
            base_price, distance_factor, quality_factor = generate_mock_data(location, oil_type)
            total_cost = calculate_total_cost(base_price, distance_factor, quality_factor)
            
            comparison_data.append({
                "Seller Location": location,
                "Base Price (USD)": base_price,
                "Transportation Factor": distance_factor,
                "Quality Factor": quality_factor,
                "Total Cost (USD)": total_cost
            })

        # Convert to DataFrame
        df = pd.DataFrame(comparison_data)
        
        # Find the cheapest option
        cheapest_option = df.loc[df["Total Cost (USD)"].idxmin()]
        
        # Display Results
        st.markdown("### Cost Analysis Results")
        st.markdown(f"**Analysis Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        st.markdown(f"**Selected Oil Type:** {oil_type}")
        
        # Display comparison table
        st.markdown("#### Cost Comparison Table")
        st.dataframe(df.style.format({
            "Base Price (USD)": "${:.2f}",
            "Transportation Factor": "{:.3f}",
            "Quality Factor": "{:.3f}",
            "Total Cost (USD)": "${:.2f}"
        }))

        # Create bar chart
        fig = px.bar(df, 
                    x="Seller Location", 
                    y="Total Cost (USD)",
                    title="Total Cost Comparison by Location",
                    color="Seller Location")
        st.plotly_chart(fig)

        # Display recommendation
        st.markdown("### Recommendation")
        st.markdown(f"""
        Based on the analysis, the most cost-effective option is:
        - **Location:** {cheapest_option['Seller Location']}
        - **Total Cost:** ${cheapest_option['Total Cost (USD)']:.2f}
        - **Base Price:** ${cheapest_option['Base Price (USD)']:.2f}
        - **Transportation Factor:** {cheapest_option['Transportation Factor']:.3f}
        - **Quality Factor:** {cheapest_option['Quality Factor']:.3f}
        """)

        # Export options
        st.markdown("### Export Options")
        st.download_button(
            label="Download Report as CSV",
            data=df.to_csv(index=False),
            file_name=f"oil_cost_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
