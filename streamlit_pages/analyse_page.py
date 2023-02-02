import streamlit as st

from st_pages import add_page_title

import numpy as np
import altair as alt
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
from analyse import *
from streamlit_extras.colored_header import colored_header
from pandas_profiling import profile_report
from streamlit_pandas_profiling import st_profile_report

df1 = pd.read_csv('dataset_1.csv')
df2 = pd.read_csv('dataset_2.csv')
df3 = pd.read_csv('dataset_3.csv')

st.set_page_config(layout="wide")
# with open("assets/style.css") as style:
#     st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)

df1 = pd.read_csv('dataset_1.csv')
df2 = pd.read_csv('dataset_2.csv')
df3 = pd.read_csv('dataset_3.csv')

st.title("Analyse 📊")
colored_header(
    label="",
    description="",
    color_name="blue-70",
)
st.header('Choix du dataset')

option = st.selectbox(
     'Quel dataset voulez-vous choisir ?',
     ('dataset_1', 'dataset_2', 'dataset_3'))

st.write('Vous avez choisi le ', option)

if option == 'dataset_1':
    df = df1
    st.write(df1)
elif option == 'dataset_2':
    df = df2
    st.write(df2)
else:
    df = df3
    st.write(df3)



##########################################################################################################################
st.header('Compétences les plus recherchées')
n = st.select_slider("Choisissez le nombre de compétences à afficher", options=[3, 5, 7, 10, 12, 15])
top_n_skills = skills_best_n(df, n)
top_n_skills_pie_chart = pie_chart(top_n_skills,"counts","index",f"<b>Les {len(top_n_skills)} compétences les plus demandées en Ile-de-france</b>")
st.plotly_chart(top_n_skills_pie_chart)
##########################################################################################################################
st.header('Entreprises qui recrutent le plus')
n = st.select_slider("Choisissez le nombre d'entreprises à afficher", options=[3, 5, 7, 10, 12, 15])
top_n_companies = entreprises_best_n(df, n)
top_n_companies_plot = bar_plot_asc(top_n_companies, 'counts', 'index', 'index', 'index', f"Top {len(top_n_companies)} Entreprises qui recrutent le plus")
st.plotly_chart(top_n_companies_plot)
##########################################################################################################################
st.header('Postes les mieux payés')
n = st.select_slider("Choisissez le nombre de postes à afficher", options=[3, 5, 7, 10])
top_n_jobs = jobs_best_n(df, n)
top_n_jobs_barplot = bar_plot_asc(top_n_jobs,"Intitulé du poste","salaire_moyen",top_n_jobs["salaire_moyen"],"salaire_moyen",f"<b>Les {len(top_n_jobs)} postes les mieux rémunérées en Ile-de-france</b>")
st.plotly_chart(top_n_jobs_barplot)
##########################################################################################################################
st.header('Type de contrats')
n = st.select_slider("Choisissez le nombre de contrats à afficher", options=[2,3,4,5])
top_n_contrat = contrat_best_n(df, n)
top_n_contrat_paid_pie_chart = pie_chart(top_n_contrat,"counts","index",f"<b>La répartition par types de contrat en Ile-de-france</b>")
st.plotly_chart(top_n_contrat_paid_pie_chart)
##########################################################################################################################
st.header('Compétences les mieux payées')
n = st.select_slider("Choisissez le nombre de compétences à afficher", options=[5, 7, 10, 12, 15])
top_n_skills_paid = skills_best_n_paid(df,n)
top_n_skills_paid_pie_chart = pie_chart(top_n_skills_paid,"Salaire_mean","competences",f"<b>Les {len(top_n_skills_paid)} compétences les mieux rémunérées en Ile-de-france</b>")
st.plotly_chart(top_n_skills_paid_pie_chart)
##########################################################################################################################
st.header('Heatmap de la Matrice de corrélation')

option = st.selectbox(
     'Quelle méthode voulez-vous choisir ?',
     ('pearson', 'kendall', 'spearman'))
st.write('Vous avez choisi la méthode', option)

if option == 'pearson':
    method = "pearson"
elif option == 'kendall':
    method = "kendall"
else:
    method = "spearman"
    
mat_corr = matrice_corr(df,method)
corr_heatmap= heatmap(mat_corr[0],f"<b>Matrice de corrélation avec la méthode {mat_corr[1]} </b>")
st.plotly_chart(corr_heatmap)
##########################################################################################################################

if option == 'dataset_1':
    #st.write(type(dataset_1))
    pr = df1.profile_report()
    st_profile_report(pr)
#     st.write(dataset_1)
elif option == 'dataset_2':
    
    pr = df2.profile_report()
    st_profile_report(pr)
#     st.write(dataset_2)
else:
     
    pr = df3.profile_report()
    st_profile_report(pr)
#     st.write(dataset_3)


##########################################################################################################################

from cluster import *

st.header('Clustering')

option = st.selectbox(
     'Quelle dataset voulez-vous choisir ?',
     ('dataset_patrick', 'dataset_tarik', 'dataset_patrick_tarik'))
st.write('Vous avez choisi le ', option)

if option == 'dataset_patrick':
    df = df1
elif option == 'dataset_tarik':
    df = df2
else:
    df = df3
    
X = kmeans_data(df1)
plot_elbow_method(X)
cluster_plot(df1)

st.plotly_chart(plot_elbow_method(X))

st.plotly_chart(cluster_plot(df))
