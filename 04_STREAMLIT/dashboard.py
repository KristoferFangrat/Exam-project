import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from connect_data_warehouse import query_police_events

# Load data from Snowflake
df = query_police_events()

# Ensure the datetime column is properly parsed
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'])

# Debugging: Print the columns and first few rows of the DataFrame
st.write("First few rows of the DataFrame:", df.head())

# Layout för Streamlit-appen
def layout():
    st.title('Exam Project Dashboard')
    st.write('Här kan du se data från polisens API.')

    # Filter options
    cities = df['city'].unique().tolist() if 'city' in df.columns else []
    municipalities = df['municipality'].unique().tolist() if 'municipality' in df.columns else []

    selected_city = st.selectbox('Select City', cities) if len(cities) > 0 else None
    selected_municipality = st.selectbox('Select Municipality', municipalities) if len(municipalities) > 0 else None

    # Date range filter
    filtered_df = df.copy()
    if 'date' in filtered_df.columns:
        start_date = st.date_input('Start date', filtered_df['date'].min())
        end_date = st.date_input('End date', filtered_df['date'].max())
        filtered_df = filtered_df[(filtered_df['date'] >= pd.to_datetime(start_date)) & (filtered_df['date'] <= pd.to_datetime(end_date))]

    # Filter data based on selection
    if selected_city:
        filtered_df = filtered_df[filtered_df['city'] == selected_city]
    if selected_municipality:
        filtered_df = filtered_df[filtered_df['municipality'] == selected_municipality]

    # Visa data
    st.write(filtered_df)

    # Summary statistics
    st.subheader('Summary Statistics')
    st.write(filtered_df.describe())

    # Interactive map
    if 'latitude' in filtered_df.columns and 'longitude' in filtered_df.columns:
        st.map(filtered_df[['latitude', 'longitude']])

    # Interaktiv graf för att jämföra olyckor med och utan nederbörd
    st.subheader('Traffic Accidents on Days with and without Precipitation')
    if 'precipitation' in filtered_df.columns:
        accidents_with_precipitation = filtered_df[filtered_df['precipitation'] > 0].shape[0]
        accidents_without_precipitation = filtered_df[filtered_df['precipitation'] == 0].shape[0]

        fig, ax = plt.subplots()
        ax.bar(['With Precipitation', 'Without Precipitation'], [accidents_with_precipitation, accidents_without_precipitation], color=['blue', 'orange'])
        ax.set_xlabel('Condition')
        ax.set_ylabel('Number of Accidents')
        ax.set_title('Number of Traffic Accidents on Days with and without Precipitation')
        st.pyplot(fig)
    else:
        st.write("Column 'precipitation' is not available in the data.")

    # Download data
    st.subheader('Download Data')
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download data as CSV", data=csv, file_name='filtered_data.csv', mime='text/csv')

if __name__ == '__main__':
    layout()