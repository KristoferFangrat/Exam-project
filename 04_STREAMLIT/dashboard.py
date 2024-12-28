import streamlit as st
from connect import query_events
import pandas as pd
import numpy as np
import plotly.express as px

def layout():
    global df
    df = query_events()
    def map():
            st.subheader("Information om händelse")

            fig = px.scatter_mapbox(filtered_data, lat="LATITUDE",
                                    lon="LONGITUDE",
                                    hover_name="LOCATION",
                                    hover_data=[ "CATEGORY"],
                                    color_discrete_sequence=["red"],
                                    zoom=4, height=800)
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
            if selected_event['TEMPERATURE'] > 0 and selected_event['PRECIPITATION'] > 0:
                st.write(f"**Precipitation:** {selected_event['PRECIPITATION']} mm:rain_cloud:")
            elif selected_event['TEMPERATURE'] < 0 and selected_event['PRECIPITATION'] > 0:
                st.write(f"**Precipitation:** {selected_event['PRECIPITATION']} mm:snow_cloud:")
                # st.snow()
            else:
                st.write(f"**Precipitation:** {selected_event['PRECIPITATION']} mm")
            
    menu = ["Home", "Event Finder", "About"]
    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        st.title("Polisens händelseöversikt")
        st.image("C:/Users/Timot/Documents/github/examensarbete/Policebackgroung.png")
        col1, col2, col3 = st.columns(3)
        event_count = len(df["EVENT"])
        col1.metric("Antal händelser:police_car:", event_count)
        traffic = (df["CATEGORY"] == "Trafikolycka").sum()
        col2.metric("Antal trafikolyckor:ambulance:", traffic)
        col3.metric("Händelser per dag:rotating_light:", round(event_count / 30, 1))
        
        st.write('''På den här sidan hittar du statistik och information om svenska polisens händelser ute i fält. 
                 Titta i statistiken eller sök efter specifika händelser. Utöver Polisens händerlser så kan du då en insikt 
                 över väderförhållanden på plats.''')
        
        st.write('''Nedan ser vi top 5 händelser per kategori''')
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
        st.write('''Här visas top 5 antal händelser per ort.''')
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
        st.write('''Här visas de fem kallaste platserna där event har skett.''')
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
        st.write('''Här visas de fem varmaste platserna där event har skett''')
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
        st.write('''Här kan man filtrera fram nederbörd per ort.''')
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
        st.title("Hitta en händelse")
        find = st.selectbox("Hur vill du söka fram händelser?", ["Kategori", "Plats", "Datum"], index=None, placeholder="Välj alternativ")
        if find == "Kategori":
            selected_category = st.selectbox("Välj en kategori:", df["CATEGORY"].unique())
            filtered_data = df[df["CATEGORY"] == selected_category]
            map()
        elif find == "Plats":
            selected_category = st.selectbox("Välj en plats:", df["LOCATION"].unique())
            filtered_data = df[df["LOCATION"] == selected_category]
            map()
        elif find == "Datum":
            options = sorted(df["TIME"].unique().tolist()) 

            selected_category = st.select_slider("Välj en tid:", options)
            filtered_data = df[df["TIME"] == selected_category]
            map()
        else:
            st.write("Inget valt")



        
        
        
        
        

        
    else:
        st.subheader("Om")
        st.write('''Välkommen till vår visualiseringssida – en del av vårt examensarbete! 🎓

Den här sidan är skapad med syftet att presentera data på ett snyggt och användarvänligt sätt, samtidigt som vi testar våra kunskaper och utmanar oss själva under vår utbildning. Observera att allt innehåll på den här sidan är resultatet av ett studentprojekt, vilket betyder att det kan finnas buggar, felaktigheter eller till och med något som är rent hittepå (vi lovar att vi försökt vårt bästa dock!).

Ansvarsfriskrivning:
Informationen som visas här ska tas med en nypa salt. Vi tar inget ansvar för hur den används, tolkas eller om den på något sätt påverkar din dag negativt. Har du feedback, funderingar eller bara vill ge oss en klapp på axeln för vårt arbete? Hör gärna av dig!

Tack för att du kikar in, och kom ihåg – det här är bara början på vår resa som (förhoppningsvis) framtida datanördar. 🚀

''')
        st.write(":rainbow[Obs, texten är AI genererad.]")

    


    


    
    


if __name__ == "__main__":
    layout()