import streamlit as st
from connect import query_events
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder
def layout():
    df = query_events()
    
    menu = ["Home", "Event Finder", "About"]

    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Home":
        st.title("Polisens händelseöversikt")
        st.write('''På den här sidan hittar du statistik och information om svenska polisens händelser ute i fält. 
                 Titta i statistiken eller sök efter specifika händelser. Utöver Polisens händerlser så kan du då en insikt 
                 över väderförhållanden på plats.''')
        cols_1 = st.columns(2)
        cols_2 = st.columns(2)
        with cols_1[0]:
            st.bar_chart(
            query_events(
                """
                    SELECT 
                        COUNT(CATEGORY) as AMOUNT_CATEGORY,
                        CATEGORY
                    FROM 
                        mart_events
                    GROUP BY 
                        CATEGORY
                    ORDER BY AMOUNT_CATEGORY DESC LIMIT 5;
                    """
            ),
            x="CATEGORY",
            y="AMOUNT_CATEGORY",
            )
        with cols_1[1]:
            st.bar_chart(
            query_events(
                """
                    SELECT 
                        COUNT(LOCATION) as TOT_EVENTS,
                        LOCATION
                    FROM 
                        mart_events
                    GROUP BY 
                        LOCATION
                    ORDER BY TOT_EVENTS DESC LIMIT 5;
                    """
            ),
            x="LOCATION",
            y="TOT_EVENTS",
            )
        with cols_2[0]:
           st.bar_chart(
            query_events(
                """
                    SELECT 
                        MIN(TEMPERATURE) as MIN_TEMPERATURE,
                        LOCATION
                    FROM 
                        mart_events
                    GROUP BY 
                        LOCATION
                    ORDER BY MIN_TEMPERATURE ASC LIMIT 5;
                    """
            ),
            x="LOCATION",
            y="MIN_TEMPERATURE",
            ) 
        with cols_2[1]:
           st.bar_chart(
            query_events(
                """
                    SELECT 
                        MAX(TEMPERATURE) as MAX_TEMPERATURE,
                        LOCATION
                    FROM 
                        mart_events
                    GROUP BY 
                        LOCATION
                    ORDER BY MAX_TEMPERATURE DESC LIMIT 5;
                    """
            ),
            x="LOCATION",
            y="MAX_TEMPERATURE",
            )

        selected_location = st.selectbox("Select a location:", df["LOCATION"].unique())
        
        st.line_chart(
            query_events(
                f"""
                    SELECT 
                        TIME,
                        PRECIPITATION,
                        LOCATION
                    FROM 
                        mart_events
                    WHERE 
                        LOCATION = '{selected_location}'
                    ;
                """
            ),
            x="TIME",
            y="PRECIPITATION",
            )
        
    

    elif choice == "Event Finder":
        st.title("Find an Event")
        selected_category = st.selectbox("Select a category:", df["CATEGORY"].unique())

        st.subheader("Event Information")
        filtered_data = df[df["CATEGORY"] == selected_category]
        fig = px.scatter_mapbox(filtered_data, lat="LATITUDE", lon="LONGITUDE", hover_name="LOCATION", hover_data=[ "CATEGORY"], color_discrete_sequence=["red"],zoom=4, height=800)

        fig.update_layout(mapbox_style="open-street-map")
        st.plotly_chart(fig)
        sorted_events = sorted(filtered_data["EVENT"].unique())
        selected_event_name = st.selectbox("Select a event:", filtered_data["EVENT"].unique())
        selected_event = filtered_data[filtered_data["EVENT"] == selected_event_name].iloc[0]

        st.write(f"**Category:** {selected_event['CATEGORY']}")
        st.write(f"**Event:** {selected_event['EVENT']}")
        st.write(f"**Location:** {selected_event['LOCATION']}")
       
        st.write(f"**Summary:** {selected_event['SUMMARY']}")
        st.write(f"**Time:** {selected_event['TIME']}")
        st.write(f"**Temperature:** {selected_event['TEMPERATURE']}°C")
        st.write(f"**Precipitation:** {selected_event['PRECIPITATION']} mm")
        

        
    else:
        st.subheader("About")
    

    


    


    
    


if __name__ == "__main__":
    layout()