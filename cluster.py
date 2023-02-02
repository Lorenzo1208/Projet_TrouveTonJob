from data_cleaning import get_dataset_1,get_dataset_2, get_dataset_3
import pandas as pd
import datetime
from sklearn.cluster import KMeans, MeanShift
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist
import numpy as np
import matplotlib.pyplot as plt

vectorizer = CountVectorizer()
df1 = get_dataset_1()
df2 = get_dataset_2()
df3 = get_dataset_3()

def kmeans_data(df= pd.DataFrame()):
  
    df = df.drop(columns='origine')
    df.dropna(inplace=True)
    df = df[df['Salaire minimum'] < 300000]
    df.dropna(subset=['Salaire minimum', 'Salaire maximum'], inplace=True)
    df['competences'] = df['competences'].apply(lambda x : x.replace(', ', ' ').replace(',', ' '))

    df['Date de publication'] = pd.to_datetime(df['Date de publication'])
    df['Date de publication'] = df['Date de publication'].apply(lambda x: x.timestamp())
    df['Date de publication'] = df['Date de publication'].astype(int)

    df = pd.get_dummies(df, columns=["Intitulé du poste",'lieu', 'Nom de la société','competences', 'Type de contrat'])
    imputer = SimpleImputer(strategy='median')
    df["Date de publication"] = imputer.fit_transform(df[["Date de publication"]])

    scaler = MinMaxScaler()
    df["Salaire minimum"] = scaler.fit_transform(df[["Salaire minimum"]])
    df["Salaire maximum"] = scaler.fit_transform(df[["Salaire maximum"]])
    df["Date de publication"] = scaler.fit_transform(df[["Date de publication"]])
    X = df.values
    kmeans = KMeans()
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)
    return X



def plot_elbow_method(X):
    K = range(1, 20)
    inertias = []

    for k in K:
        kmeanModel = KMeans(n_clusters=k).fit(X)
        kmeanModel.fit(X)
        inertias.append(kmeanModel.inertia_)
  
    fig = px.line(x=K, y=inertias, labels={'x': 'Valeurs de K', 'y': 'Inertie'})
    fig.update_layout(title='Méthode du coude')
    res = fig
    return res


def cluster_plot(df):
    X = kmeans_data(df)
    inertias = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k)
        kmeans.fit(X)
        inertias.append(kmeans.inertia_)

    optimal_k = np.argmin(inertias) + 1
    kmeans = KMeans(n_clusters=optimal_k)
    kmeans.fit(X)
    y_kmeans = kmeans.predict(X)

    fig = px.scatter(x=X[:, 0], y=X[:, 1], color=y_kmeans, color_discrete_sequence='viridis')
    centers = kmeans.cluster_centers_
    fig.add_scatter(x=centers[:, 0], y=centers[:, 1], mode='markers', marker=dict(size=12, color='red', symbol='x'))
    fig.update_layout(title='Clustering des offres d\'emploi')
    res = fig
    return res


X = kmeans_data(df1)
plot_elbow_method(X)
cluster_plot(df1)
