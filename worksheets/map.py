import streamlit as st
import pandas as pd
from connect_data_warehouse import query_events

def main():
    st.title("Event Map")
    menu = ["Home", "Category", "Location", "Percipitation", "Temperature"]

    choice = st.sidebar.selectbox("Menu", menu)

    # Hämta data från Snowflake
    df = query_events()

    if choice == "Home":
        st.write("Welcome to the Home page")
        
        #st.write("DataFrame columns:", df.columns.tolist())

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

        # Display map with filtered data
        if "LATITUDE" in filtered_df.columns and "LONGITUDE" in filtered_df.columns:
            st.map(filtered_df[["LATITUDE", "LONGITUDE"]])
        else:
            st.warning("Latitude and longitude columns are missing in the data.")
        
        # Display events in a selectbox
        if "EVENT" in filtered_df.columns:
            event_options = filtered_df["EVENT"].unique().tolist()
            selected_event = st.selectbox("Select Event", event_options)
            
            event_details = filtered_df[filtered_df["EVENT"] == selected_event]
            
            # Display event details
            st.write("Event Details:")
            st.write(event_details)
        else:
            st.warning("Event column is missing in the data.")
        
    elif choice == "Category":
        st.write("Category page")
        if "CATEGORY" in df.columns:
            category_options = ["All"] + df["CATEGORY"].unique().tolist()
            selected_category = st.selectbox("Select Category", category_options)
            
            if selected_category == "All":
                filtered_df = df
            else:
                filtered_df = df[df["CATEGORY"] == selected_category]
            
            if not filtered_df.empty:
                st.map(filtered_df[['LATITUDE', 'LONGITUDE']])
                st.dataframe(filtered_df)
            else:
                st.warning("No data found for the selected category.")
        else:
            st.warning("Category column is missing in the data.")
    elif choice == "Location":
        st.write("Location page")
        location = st.text_input("Enter location")
        if location:
            filtered_df = df[df['LOCATION'].str.contains(location, case=False, na=False)]
            if not filtered_df.empty:
                st.map(filtered_df[['LATITUDE', 'LONGITUDE']])
                st.dataframe(filtered_df)
            else:
                st.warning("No data found for the entered location.")
    elif choice == "Temperature":
        st.write("Temperature page")
        # Add your temperature-specific code here
    
    #st.dataframe(df)

if __name__ == "__main__":
    main()