import string
import pandas as pd
import numpy as np
import requests
import unidecode

url = "https://raw.githubusercontent.com/Lorenzo1208/Projet_TrouveTonJob/main/data.json"

try:
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame(data)

except:
    print(f"Erreur de chargement du lien - {url}")
    quit()


liste_salaires = df['lieu'].apply(lambda x : x[1] if len(x) > 1 else '')

df['lieu'] = df['lieu'].apply(lambda x : x[0])

df['Nom de la société'] = df['Type de poste'].apply(lambda x : x[2] if len(x) > 2 else '')
df['Type de contrat'] = df['Type de poste'].apply(lambda x : x[7].split(' - ')[0] if len(x) > 7 else '')
df.drop(columns='Type de poste', inplace=True)

df = df.apply(lambda c : c.apply(lambda x : ','.join([s.strip("\n ").lower() for s in (x.split(',') if type(x) != list else x)])))

liste_dates = df['Date de publication'].apply(lambda x: '0 j' if x.find('heures') != -1 else x.removeprefix('postée il y a ').replace('postée hier', '1 j').strip('iours'))

df['Date de publication'] = pd.to_datetime(liste_dates.apply(
    lambda x :
        pd.to_datetime("2023-01-15") - pd.DateOffset(months=int(x.split()[0])) if x.split()[1] == 'm'
        else pd.to_datetime("2023-01-15") - pd.DateOffset(days=int(x.split()[0]))
    ))

df['Salaire minimum'] = liste_salaires.apply(lambda x : float(x.split(' - ')[0].strip(' €\n').replace('.', '').replace(',', '.')) if x != '' else np.nan)
df['Salaire maximum'] = liste_salaires.apply(lambda x : float(x.split(' - ')[1].strip(' €/an\n' + string.ascii_letters).replace('.', '').replace(',', '.')) if x != '' else np.nan)

noms_ville = ['la defense', 'guyancourt', 'antony', 'paris']

df['lieu'] = df['lieu'].apply(
    lambda x : (
        [n for n in noms_ville for i in unidecode.unidecode(x).replace(' - ', ',').replace('-', ' ').split(',') if n in i] +
        [unidecode.unidecode(x).replace('-', ' ')]
        )[0]
    )

#remplace si data analyst dans vavlue par data analyste etc
terms_to_replace = {'analyst': 'data analyst', 'datascientist': 'data scientist', 'data engineer': 'ingénieur'}
df["Intitulé du poste"] = df["Intitulé du poste"].apply(lambda x: ' '.join([terms_to_replace.get(term, term) for term in unidecode.unidecode(x).split()]))

keywords = ["business analyst","analyste fonctionnel","architecte","apprenti","data ingenieur", "data engineer","data analyst","data scientist","consultant","ingenieur","chef de projet","concepteur","alternance","stage",
            "technical leader","technicien","responsable","référent","expert","developpeur"]

for keyword in keywords:
    df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"(.*{keyword})", keyword, regex=True)
    df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"({keyword}.*)", keyword, regex=True)

df.to_csv("data_test1.csv")