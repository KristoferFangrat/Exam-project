import streamlit as st
from connect import query_events


def layout():
    df = query_events()
    st.title("New title")
    st.write('''This dashboard displays educational ads sourced from Arbetsförmedlingen's API.:hibiscus:''')

    st.dataframe(df)




if __name__ == "__main__":
    layout()