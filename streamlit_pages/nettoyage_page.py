import streamlit as st

from st_pages import add_page_title

st.set_page_config(layout="wide"),
with open("assets/style.css") as style:
    st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)

add_page_title()

st.write("This is just a sample page!")