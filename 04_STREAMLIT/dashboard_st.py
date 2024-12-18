import streamlit as st
from connect_data_warehouse import query_events

def layout():
    df = query_events()
    st.title('Exam Project Dashboard')
    st.write('Här kan du se data från polisens & väder API.')

    st.dataframe(df)

if __name__ == '__main__':
    layout()