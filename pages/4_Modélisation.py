import streamlit as st
from operator import index
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import os 
# import pandas_profiling
# import streamlit_pandas_profiling
# from pandas_profiling import ProfileReport
# from streamlit_pandas_profiling import st_profile_report

st.title("Modélisation 🤖")

if os.path.exists('./dataset.csv'): 
    df = pd.read_csv('dataset.csv', index_col=None)

with st.sidebar: 
    st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
    st.title("Éstimer votre salaire 🤑")
    choice = st.radio("Navigation", ["Importer","Analyser","Modélisation", "Téléchargement"])
    st.info("Cette section vous permet d'explorer vos données et d'entrainer votre propre modèle.")

if choice == "Importer":
    st.title("Importer votre dataset 📂")
    file = st.file_uploader("Importer votre dataset 📂")
    if file: 
        df = pd.read_csv(file, index_col=None)
        df.to_csv('dataset.csv', index=None)
        st.dataframe(df)
            
if choice == "Analyser": 
    st.title("Analyser vos données 📊")
#     profile_df = df.ProfileReport()
#     st_profile_report(profile_df)

