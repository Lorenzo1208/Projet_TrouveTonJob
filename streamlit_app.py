import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

dataset_1 = pd.read_csv('dataset_1.csv', index_col=0)
dataset_2 = pd.read_csv('dataset_2.csv', index_col=0)
dataset_3 = pd.read_csv('dataset_3.csv', index_col=0)

st.header('ProjetTrouveTonJob')

st.write('Bienvenue sur TrouveTonJob ! :sunglasses:')

st.header('Choix du dataset')

option = st.selectbox(
     'Quel dataset voulez-vous choisir ?',
     ('dataset_1', 'dataset_2', 'dataset_3'))

st.write('Vous avez choisi le ', option)

if option == 'dataset_1':
    st.write(dataset_1)
elif option == 'dataset_2':
    st.write(dataset_2)
else:
    st.write(dataset_3)

