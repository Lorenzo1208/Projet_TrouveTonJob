# -*- coding: utf-8 -*-
# For loading data
import pandas as pd
import numpy as np
# !pip install pandasql
# For SQL queries
# import pandasql as ps

# For ploting graph / Visualization
import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import iplot
import plotly.figure_factory as ff

import plotly.io as io
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.preprocessing import LabelEncoder



# To show graph below the code or on same notebook
from plotly.offline import init_notebook_mode

# notion importante pour plotly il faut lui dire dans quel env il doit afficher les graphiques
# Default_renderer: 'browser'
# Available renderers:
#     ['plotly_mimetype', 'jupyterlab', 'nteract', 'vscode',
#      'notebook', 'notebook_connected', 'kaggle', 'azure', 'colab',
#      'cocalc', 'databricks', 'json', 'png', 'jpeg', 'jpg', 'svg',
#      'pdf', 'browser', 'firefox', 'chrome', 'chromium', 'iframe',
#      'iframe_connected', 'sphinx_gallery', 'sphinx_gallery_png']
# io.renderers.default = "notebook_connected"

# init_notebook_mode(connected=True)

"""##Import de nos données"""

# Import des dataset
#df1 pour les données de patrick
pd.options.display.float_format = '{:.2f}'.format
df1 = pd.read_csv("dataset_1.csv")
#df2 pour nos data "scrapper"
pd.options.display.float_format = '{:.2f}'.format
df2 = pd.read_csv("dataset_2.csv")
#df3 pour nos deux dataset combinés
pd.options.display.float_format = '{:.2f}'.format
df3 = pd.read_csv("dataset_3.csv")

"""##Vérification de nos données nulles"""

#Vérification des val nulles dans nos dataset
values_manquantes = pd.DataFrame({'df1': df1.isna().sum(), 'df2': df2.isna().sum(), 'df3': df3.isna().sum()})
values_manquantes

#dropna des df
df1 =df1.dropna()
df2 =df2.dropna()
df3 =df3.dropna()

#Vérification des val nulles dans nos dataset
values_manquantes = pd.DataFrame({'df1': df1.isna().sum(), 'df2': df2.isna().sum(), 'df3': df3.isna().sum()})
values_manquantes

df1.head()

df2.head()

df3.head()

"""## Les fonction pour les graphique
###Pie chart
"""

def pie_chart(df_input,values,names,titre='Titre du graph'):
  fig = px.pie(df_input, values=values, names=names )
  fig.update_layout(title_text=titre, title_x=0.5)
  res = fig
  return res

"""###Horizontale barplot"""

def bar_plot_asc(df_inpput,val_x,val_y,hover_name,color, titre='Titre du graphique'):
  #io.renderers.default='colab'
  df = df_inpput
  fig = px.bar(df_inpput, x=val_x, y=val_y, hover_name=hover_name , color=color)
  fig.update_layout( yaxis={'categoryorder': 'total ascending'})
  fig.update_layout(title_text=titre, title_x=0.5)
  res = fig
  return res

"""# Les compétences les plus recherchées"""

def skills_best_n(df: pd.DataFrame, num_skills:int):
  df = df.dropna(subset=["competences"])
  df = df.dropna(subset=["competences"])
  df["competences"] = df["competences"].str.split(",").apply(lambda x: [i.strip() for i in x])
  competences_count = df["competences"].explode().value_counts(dropna=True, sort=True).reset_index(name='counts')
  res = competences_count.head(num_skills)
  return res


"""# Les entreprises qui recrutent le plus"""

def entreprises_best_n(df: pd.DataFrame, num_skills:int):
  df = df.dropna(subset=["Nom de la société"])
  df["Nom de la société"] = df["Nom de la société"].str.split(",").apply(lambda x: [i.strip() for i in x])
  entreprises_count = df["Nom de la société"].explode().value_counts().reset_index(name='counts')
  res = entreprises_count.head(num_skills)
  return res  


# #box plot
# df =  top_n_jobs
# fig = px.box(df, x="salaire_moyen", y="Intitulé du poste")
# # fig.show()

"""# Les postes les mieux payés
"""

# Tarik
def jobs_best_n(df: pd.DataFrame, num_skills:int):
  df = df.dropna(subset=['Intitulé du poste','Salaire minimum','Salaire maximum'])
  df["Intitulé du poste"] = df["Intitulé du poste"]
  df["Salaire_mean"] = (df['Salaire minimum'].astype(float) + df['Salaire maximum'].astype(float)) / 2
  df = df[["Intitulé du poste","Salaire_mean"]]
  res = df.groupby(["Intitulé du poste"])["Salaire_mean"] \
                    .mean() \
                    .reset_index(name='salaire_moyen') \
                    .sort_values(['salaire_moyen'], ascending=False) \
                    .head(num_skills)
  return res



"""# Les compétences les mieux payés
# Le salaire moyen par compétence
"""

def skills_best_n_paid(df:pd.DataFrame, num_skills:int):
    df = df.dropna(subset=['competences','Salaire minimum','Salaire maximum'])
    df["Salaire_mean"] = (df['Salaire minimum'].astype(float) + df['Salaire maximum'].astype(float)) / 2
    df["competences"] = df["competences"].str.split(",").apply(lambda x: [i.strip() for i in x])
    df = df.explode('competences')
    df = df.groupby('competences')['Salaire_mean'].mean().sort_values(ascending=False).reset_index(name='Salaire_mean')
    return df.head(num_skills)


"""# Les types de contrat"""

def contrat_best_n(df: pd.DataFrame, num_skills:int):
  df = df.dropna(subset=["Type de contrat"])
  df["Type de contrat"] = df["Type de contrat"].str.split(",").apply(lambda x: [i.strip() for i in x])
  contrat_count = df["Type de contrat"].explode().value_counts().reset_index(name='counts')
  res = contrat_count.head(num_skills)
  return res  


"""##Analyse multivariée"""

def matrice_corr(df: pd.DataFrame,methode:str)->tuple:
  df['competences'] = df['competences'].astype(str)
  df['competences'] = df['competences'].apply(lambda x : x.strip())
  if methode not in ['pearson', 'kendall', 'spearman']:
        raise ValueError("Invalid method. Choose from 'pearson', 'kendall', 'spearman'.")
  df = df.drop(columns='origine')
  df['Date de publication'] = pd.to_datetime(df['Date de publication'])

  # Create a label encoder
  le = LabelEncoder()

  # Encode all the non-numeric columns
  df_encoded = df.apply(le.fit_transform)

  # Find the minimum date
  min_date = df['Date de publication'].min()

  # Create a new column 'Encoded_date' by subtracting the minimum date from the original date column
  df['Date de publication'] = (df['Date de publication'] - min_date).dt.days

  # calculate correlation matrix
  corr = df_encoded.corr(method=methode)
  return corr, methode


# Attention la fonction matrice_corr renvoie un tuple
def heatmap(corr_mat,titre='Titre du graph'):
  fig = px.imshow(corr_mat, text_auto=True,color_continuous_scale='RdBu_r')
  fig.update_layout(title_text=titre, title_x=0.5)
  res = fig
  return res


def main():
  
  #Les compétences les plus recherchées Df
  top_n_skills = skills_best_n(df2,20)
  top_n_skills
  #Les compétences les plus recherchées graphiques
  #en bar plot
  # top_n_skills_barplot = bar_plot_asc(top_n_skills,"counts","index","index","index")
  # top_n_skills_barplot
  #en pie chart solution retenue 
  
  top_n_skills_pie_chart = pie_chart(top_n_skills,"counts","index",f"<b>Les {len(top_n_skills)} compétences les plus demandées en Ile-de-france</b>")
  top_n_skills_pie_chart

  # Les entreprises qui recrutent Df
  top_n_business = entreprises_best_n(df2,15)
  top_n_business

  # Les entreprises qui recrutent graphique
  top_n_business_barplot = bar_plot_asc(top_n_business,"counts","index","index","index",f"<b>Les {len(top_n_business)} entreprises qui recrutent les plus en Ile-de-france</b>")
  top_n_business_barplot

  #Les postes les mieux payées Df
  top_n_jobs = jobs_best_n(df2,10)

  top_n_jobs
  print(top_n_jobs.head(2))
  #Les postes les mieux payées graphique
  top_n_jobs_barplot = bar_plot_asc(top_n_jobs,"Intitulé du poste","salaire_moyen",top_n_jobs["salaire_moyen"],"salaire_moyen",f"<b>Les {len(top_n_jobs)} postes les mieux rémunérées en Ile-de-france</b>")
  top_n_jobs_barplot

  #Les compétences les mieux payées Df
  top_n_skills_paid = skills_best_n_paid(df2,10)
  top_n_skills_paid

  #Les compétences les mieux payées Graphique
  top_n_skills_paid_pie_chart = pie_chart(top_n_skills_paid,"Salaire_mean","competences",f"<b>Les {len(top_n_skills_paid)} compétences les mieux rémunérées en Ile-de-france</b>")
  top_n_skills_paid_pie_chart

  # Creation df des types de contrats
  top_n_contrat = contrat_best_n(df2,10)
  top_n_contrat

  #Grapique des types de contrats
  top_n_contrat_paid_pie_chart = pie_chart(top_n_contrat,"counts","index",f"<b>La répartition par types de contrat en Ile-de-france</b>")
  top_n_contrat_paid_pie_chart

  #Matrice de coorelation
  mat_corr = matrice_corr(df2,"pearson")
  mat_corr

  #Matrice de coorelation heatmap
  corr_heatmap= heatmap(mat_corr[0],f"<b>Matrice de corrélation avec la méthode {mat_corr[1]} </b>")
  corr_heatmap
if __name__ == '__main__':
    main()
