import streamlit as st
import pandas as pd
import numpy as np
from connect_data_warehouse import query_events

def layout():
    df = query_events()
    st.title("New title")
    st.write('''This dashboard displays educational ads sourced from Arbetsförmedlingen's API.:hibiscus:''')

    # Print DataFrame columns
    st.write("DataFrame columns:", df.columns.tolist())

    # Filter data based on location
    if "LOCATION" in df.columns:
        location_options = ["All"] + df["LOCATION"].unique().tolist()
        selected_location = st.selectbox("Select Location", location_options)
        
        if selected_location == "All":
            filtered_df = df
        else:
            filtered_df = df[df["LOCATION"] == selected_location]
        
        with st.container():
            # Create columns
            col1, col2, col3, col4, col5 = st.columns(5)

            # Display metrics in columns
            col1.markdown(f"<p style='font-size:20px;'>Total Events: {filtered_df.shape[0]}</p>", unsafe_allow_html=True)
            
            if "CATEGORY" in filtered_df.columns:
                total_categories = filtered_df["CATEGORY"].nunique()
                col2.markdown(f"<p style='font-size:20px;'>Total Categories: {total_categories}</p>", unsafe_allow_html=True)
                top_category = filtered_df["CATEGORY"].value_counts().idxmax()
                col3.markdown(f"<p style='font-size:20px;'>Most Frequent Category: {top_category}</p>", unsafe_allow_html=True)
            else:
                st.warning("Category column is missing in the data.")
            
            if "LOCATION" in filtered_df.columns:
                top_kommun = filtered_df["LOCATION"].value_counts().idxmax()
                col4.markdown(f"<p style='font-size:20px;'>Top Kommun: {top_kommun}</p>", unsafe_allow_html=True)
            else:
                st.warning("Kommun column is missing in the data.")
            
            if "TEMPERATURE" in filtered_df.columns:
                lowest_temperature = filtered_df["TEMPERATURE"].min()
                col5.markdown(f"<p style='font-size:20px;'>Lowest Temperature: {lowest_temperature}</p>", unsafe_allow_html=True)
            else:
                st.warning("Temperature column is missing in the data.")

        if "LATITUDE" in filtered_df.columns and "LONGITUDE" in filtered_df.columns:
            st.map(filtered_df[["LATITUDE", "LONGITUDE"]])
        else:
            st.warning("Latitude and longitude columns are missing in the data.")
        
        st.dataframe(filtered_df)
    else:
        st.warning("Location column is missing in the data.")

if __name__ == "__main__":
    layout()