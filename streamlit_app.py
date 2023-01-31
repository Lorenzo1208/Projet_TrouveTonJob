from pathlib import Path
import streamlit as st
from st_pages import Page, add_page_title, show_pages
st.set_page_config(layout="wide"),
with open("assets/style.css") as style:
    st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)
show_pages(
        [
            
            Page("streamlit_app.py", "Le Projet", ""),
            # Can use :<icon-name>: or the actual icon
            Page("streamlit_pages/data_profiling_page.py", "Data Profiling", ""),
            # The pages appear in the order you pass them
            Page("streamlit_pages/nettoyage_page.py", "Nettoyage", ""),
            Page("streamlit_pages/analyse_page.py", "Analyse descriptive et exploratoire", ""),
            # Will streamlit_pagesuse the default icon and name based on the filename if you don't
            # pass them
            Page("streamlit_pages/modelisation_page.py","Modélisation en Machine learning"),
            Page("streamlit_pages/app_web_page.py", "L'application web", ""),
        ]
    )
'''
# Trouve ton job dans l'IA
'''
st.write('Bienvenue sur TrouveTonJob ! :sunglasses:')   
'''
Analyser des données d'offres d'emploi en rapport avec votre futur métier dans l'IA

## Contexte du projet
En tant que futur développeur IA vous allez vous familiariser avec le marché de l'emploi du secteur.

A partir d'un jeu de données fourni (issu du web scraping), vous allez réaliser le/la :

'''
st.markdown("- Intégration des données")
st.markdown("- Nettoyage")
st.markdown("- Préparation")
st.markdown("- Analyse descriptive et exploratoire")
st.markdown("- Modélisation grâce au machine learning")
st.markdown("- Développement d'une application web")
st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
</style>
''', unsafe_allow_html=True)
    



