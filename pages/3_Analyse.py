import streamlit as st
from analyse import *

st.title("Analyse")

df1 = pd.read_csv('dataset_1.csv')
df2 = pd.read_csv('dataset_2.csv')
df3 = pd.read_csv('dataset_3.csv')

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
top_n_skills = skills_best_n(df,10)
top_n_skills_pie_chart = pie_chart(top_n_skills,"counts","index",f"<b>Les {len(top_n_skills)} compétences les plus demandées en Ile-de-france</b>")
st.plotly_chart(top_n_skills_pie_chart)
##########################################################################################################################
st.header('Entreprises qui recrutent le plus')
top_n_companies = entreprises_best_n(df, 10)
top_n_companies_plot = bar_plot_asc(top_n_companies, 'counts', 'index', 'index', 'index', f"Top {len(top_n_companies)} Entreprises qui recrutent le plus")
st.plotly_chart(top_n_companies_plot)
##########################################################################################################################
st.header('Postes les mieux payés')
top_n_jobs = jobs_best_n(df,10)
top_n_jobs_barplot = bar_plot_asc(top_n_jobs,"Intitulé du poste","salaire_moyen",top_n_jobs["salaire_moyen"],"salaire_moyen",f"<b>Les {len(top_n_jobs)} postes les mieux rémunérées en Ile-de-france</b>")
st.plotly_chart(top_n_jobs_barplot)
##########################################################################################################################
st.header('Type de contrats')
top_n_contrat = contrat_best_n(df,10)
top_n_contrat_paid_pie_chart = pie_chart(top_n_contrat,"counts","index",f"<b>La répartition par types de contrat en Ile-de-france</b>")
st.plotly_chart(top_n_contrat_paid_pie_chart)
##########################################################################################################################
st.header('Compétences les mieux payées')
top_n_skills_paid = skills_best_n_paid(df,10)
top_n_skills_paid_pie_chart = pie_chart(top_n_skills_paid,"Salaire_mean","competences",f"<b>Les {len(top_n_skills_paid)} compétences les mieux rémunérées en Ile-de-france</b>")
st.plotly_chart(top_n_skills_paid_pie_chart)
##########################################################################################################################
st.header('Heatmap de la Matrice de corrélation')
mat_corr = matrice_corr(df,"pearson")
corr_heatmap= heatmap(mat_corr[0],f"<b>Matrice de corrélation avec la méthode {mat_corr[1]} </b>")
st.plotly_chart(corr_heatmap)
##########################################################################################################################
