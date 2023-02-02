
from data_cleaning import get_dataset_1,get_dataset_2, get_dataset_3
import pandas as pd
import datetime
from sklearn.cluster import KMeans, MeanShift
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import MinMaxScaler

vectorizer = CountVectorizer()
df1 = get_dataset_1()
df2 = get_dataset_2()
df3 = get_dataset_3()
df1 = df1.drop(columns='origine')
df1.dropna(inplace=True)

df1 = df1[df1['Salaire minimum'] < 300000]
df1.dropna(subset=['Salaire minimum', 'Salaire maximum'], inplace=True)
df1['competences'] = df1['competences'].apply(lambda x : x.replace(', ', ' ').replace(',', ' '))

df1['Date de publication'] = pd.to_datetime(df1['Date de publication'])
df1['Date de publication'] = df1['Date de publication'].apply(lambda x: x.timestamp())
df1['Date de publication'] = df1['Date de publication'].astype(int)

# X_poste = vectorizer.fit_transform(df_patrick["Intitulé du poste"])
# X_competences = vectorizer.transform(df_patrick["competences"])
df1 = pd.get_dummies(df1, columns=["Intitulé du poste",'lieu', 'Nom de la société','competences', 'Type de contrat'])
imputer = SimpleImputer(strategy='median')
df1["Date de publication"] = imputer.fit_transform(df1[["Date de publication"]])
# Scale the values to the range [0, 1]
scaler = MinMaxScaler()
df1["Salaire minimum"] = scaler.fit_transform(df1[["Salaire minimum"]])
df1["Salaire maximum"] = scaler.fit_transform(df1[["Salaire maximum"]])
df1["Date de publication"] = scaler.fit_transform(df1[["Date de publication"]])
X = df1.values
kmeans = MeanShift()
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

fig,ax = plt.subplots(1,3)
ax[0].scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
ax[0].scatter(centers[:, 0], centers[:, 1], c=range(len(centers)), s=200, alpha=0.5, marker='x')

df2 = df2.drop(columns='origine')
df2.dropna(inplace=True)

df2 = df2[df2['Salaire minimum'] < 300000]
df2.dropna(subset=['Salaire minimum', 'Salaire maximum'], inplace=True)
df2['competences'] = df2['competences'].apply(lambda x : x.replace(', ', ' ').replace(',', ' '))

df2['Date de publication'] = pd.to_datetime(df2['Date de publication'])
df2['Date de publication'] = df2['Date de publication'].apply(lambda x: x.timestamp())
df2['Date de publication'] = df2['Date de publication'].astype(int)

# X_poste = vectorizer.fit_transform(df_patrick["Intitulé du poste"])
# X_competences = vectorizer.transform(df_patrick["competences"])
df2 = pd.get_dummies(df2, columns=["Intitulé du poste",'lieu', 'Nom de la société','competences', 'Type de contrat'])
imputer = SimpleImputer(strategy='median')
df2["Date de publication"] = imputer.fit_transform(df2[["Date de publication"]])
# Scale the values to the range [0, 1]
scaler = MinMaxScaler()
df2["Salaire minimum"] = scaler.fit_transform(df2[["Salaire minimum"]])
df2["Salaire maximum"] = scaler.fit_transform(df2[["Salaire maximum"]])
df2["Date de publication"] = scaler.fit_transform(df2[["Date de publication"]])
X = df2.values
kmeans = MeanShift()
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

ax[1].scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
ax[1].scatter(centers[:, 0], centers[:, 1], c=range(len(centers)), s=200, alpha=0.5,marker='x')



df3 = df3.drop(columns='origine')
df3.dropna(inplace=True)

df3 = df3[df3['Salaire minimum'] < 300000]
df3.dropna(subset=['Salaire minimum', 'Salaire maximum'], inplace=True)
df3['competences'] = df3['competences'].apply(lambda x : x.replace(', ', ' ').replace(',', ' '))

df3['Date de publication'] = pd.to_datetime(df3['Date de publication'])
df3['Date de publication'] = df3['Date de publication'].apply(lambda x: x.timestamp())
df3['Date de publication'] = df3['Date de publication'].astype(int)

# X_poste = vectorizer.fit_transform(df_patrick["Intitulé du poste"])
# X_competences = vectorizer.transform(df_patrick["competences"])
df3 = pd.get_dummies(df3, columns=["Intitulé du poste",'lieu', 'Nom de la société','competences', 'Type de contrat'])
imputer = SimpleImputer(strategy='median')
df3["Date de publication"] = imputer.fit_transform(df3[["Date de publication"]])
# Scale the values to the range [0, 1]
scaler = MinMaxScaler()
df3["Salaire minimum"] = scaler.fit_transform(df3[["Salaire minimum"]])
df3["Salaire maximum"] = scaler.fit_transform(df3[["Salaire maximum"]])
df3["Date de publication"] = scaler.fit_transform(df3[["Date de publication"]])
X = df3.values
kmeans = MeanShift()
kmeans.fit(X)
y_kmeans = kmeans.predict(X)

ax[2].scatter(X[:, 0], X[:, 1], c=y_kmeans, s=50, cmap='viridis')
centers = kmeans.cluster_centers_
ax[2].scatter(centers[:, 0], centers[:, 1], c=range(len(centers)), s=200, alpha=0.5,marker='x')
plt.show()
