import streamlit as st

from st_pages import add_page_title
st.set_page_config(layout="wide"),
with open("assets/style.css") as style:
    st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)

add_page_title()

st.title("Modélisation 🤖")


st.text_input("Job recherché")
st.text_input("Vos compétences")

with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("Éstimer votre salaire 🤑")
    choice = st.radio("Navigation", ["Importer","Analyser","Modélisation", "Téléchargement"])
    st.info("Cette section vous permet d'explorer vos données et d'entrainer votre propre modèle.")
