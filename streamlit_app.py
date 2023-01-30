import numpy as np
import altair as alt
import pandas as pd
import streamlit as st

st.header('ProjetTrouveTonJob')

# Example 1

st.write('Bienvenue sur TrouveTonJob ! :sunglasses:')

# Example 2

st.write(1234)

# Example 3

df = pd.read_csv('dataset_1.csv', index_col=0)
df2 = pd.read_csv('dataset_3.csv', index_col=0)

# Example 4

st.write('Dataset nettoyé de Patrick.', df, 'Dataset nettoyé de Tarik combiné avec celui de Patrick.', df2)
