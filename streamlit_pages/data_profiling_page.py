import streamlit as st
import numpy as np
import altair as alt
import pandas as pd
from st_pages import Page, add_page_title, show_pages
from streamlit_extras.colored_header import colored_header
import pandas_profiling
from streamlit_pandas_profiling import st_profile_report

df1 = pd.read_csv('dataset_1.csv')
df2 = pd.read_csv('dataset_2.csv')
df3 = pd.read_csv('dataset_3.csv')



st.set_page_config(layout="wide")
# with open("assets/style.css") as style:
#     st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)

st.title("Data Profiling 📥")
colored_header(
    label="",
    description="",
    color_name="red-70",
)
video_file = open('assets/Webscrapping_exemple.mp4', 'rb')
video_bytes = video_file.read()

html_string =f'''
<h2><b>Le webscrapping c'est quoi?</b></h2>
<p>Recueillir des données sur le web est parfois compliqué et quand cela est possible,
 il est difficile de pouvoir les télécharger ou d’effectuer un copier-coller. 
 Le web scraping est une technique permettant l’extraction des données d’un site via un programme, un logiciel automatique ou un autre site.
 L’objectif est donc d’extraire le contenu d’une page d’un site de façon structurée.
 Le scraping permet ainsi de pouvoir réutiliser ces données.</p>
<h2><b>Dans quel cas utiliser le web scraping ?</b></h2>
 <p>L’intérêt principal du web scraping est de pouvoir récolter du contenu sur un site web, qui ne peut être copié collé sans dénaturer la structure même du document.
 Ainsi cette technique est souvent utilisée dans le cadre d’une veille concurrentielle, notamment sur des sites e-commerce.</p>
 <h2><b>Le webscrapping dans notre projet</b></h2>
 <p>Afin d'étofer le dataset qui nous avait été fourni.
 Nous avons réalisé un script python à l'aide des librairies <b>Sélenium</b></p> et <b>Beautifulsoup (Bs4)</b>
 lien.<br>
 <span>&#8226;&emsp;<a href=" ""https://beautiful-soup-4.readthedocs.io/en/latest/">la documentation Beautifulsoup</a>.</span><br>
 <span>&#8226;&emsp;<a href=" ""https://selenium-python.readthedocs.io/">la documentation Sélenium</a>.</span>
<h2><center><b>Ce que fait le script en video:</b></h2>
'''
st.markdown(html_string, unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    html_websrapping ='''
    <div class="video_comentaire">
    <p>Nous commencons d'abord par rentrer un ou des mots clées ici le keyword est Data.</br>
    Ensuite nous entrons la localisation ici 11R qui correspond sur le site de pôle emploi à la région Ile de france.</br>
    Efin la magie s'opère la librairie Bs4 va nous permètre de lire le code HTML et récupérer le contenu des balises 
    que l'on a ciblés et Sélenium va simuler les cliques de l'utilisateur.</p>
    </div>'''
    st.markdown(html_websrapping, unsafe_allow_html=True)
    
with col2:
   st.video(video_bytes, format="video/mp4", start_time=0)
