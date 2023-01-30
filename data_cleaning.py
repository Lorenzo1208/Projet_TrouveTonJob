import locale
import re
import string
from datetime import datetime

import numpy as np
import pandas as pd
import requests
import unidecode

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


def try_download_json(url:str) -> pd.DataFrame:

    try:
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data)

    except:
        print(f"Erreur de chargement du lien - {url}")
        #quit()


def try_read_csv(file) -> pd.DataFrame:

    try:
        return pd.read_csv(file, index_col=0)

    except:
        print(f"Erreur de lecture du csv - {file}")
        #quit()


def clean_data_1(df:pd.DataFrame) -> pd.DataFrame:

    liste_salaires = df['lieu'].apply(lambda x : x[1] if len(x) > 1 else '')

    df['lieu'] = df['lieu'].apply(lambda x : x[0])

    df['Nom de la société'] = df['Type de poste'].apply(lambda x : x[2] if len(x) > 2 else '')
    df['Type de contrat'] = df['Type de poste'].apply(lambda x : x[7].split(' - ')[0] if len(x) > 7 else '')
    df.drop(columns='Type de poste', inplace=True)

    df = df.apply(lambda c : c.apply(lambda x : ','.join([unidecode.unidecode(s).strip("\n ").lower() for s in (x.split(',') if type(x) != list else x)])))

    liste_dates = df['Date de publication'].apply(lambda x: '0 j' if x.find('heures') != -1 else x.removeprefix('postee il y a ').replace('postee hier', '1 j').strip('iorsu'))

    df['Date de publication'] = pd.to_datetime(liste_dates.apply(
        lambda x :
            pd.to_datetime("2023-01-15") - (pd.DateOffset(months=int(x.split()[0])) if x.split()[1] == 'm' else pd.DateOffset(days=int(x.split()[0])))
        ))

    df['Salaire minimum'] = liste_salaires.apply(lambda x : float(x.split(' - ')[0].strip(' €\n').replace('.', '').replace(',', '.')) if x != '' else np.nan)
    df['Salaire maximum'] = liste_salaires.apply(lambda x : float(x.split(' - ')[1].strip(' €/an\n' + string.ascii_letters).replace('.', '').replace(',', '.')) if x != '' else np.nan)

    noms_ville = ['la defense', 'guyancourt', 'antony', 'paris']

    df['lieu'] = df['lieu'].apply(
        lambda x :
            ([n for n in noms_ville for i in x.replace(' - ', ',').replace('-', ' ').split(',') if n in i] + [x.replace('-', ' ')])[0]
        )

    #remplace si data analyst dans vavlue par data analyste etc
    terms_to_replace = {'analyst': 'data analyst', 'datascientist': 'data scientist', 'data engineer': 'ingenieur','conultant/analyste': 'consultant/analyste','2018788': '',
                        'developer': 'developpeur','full stacke': 'developpeur','global technical seo manager': 'manager','engineer': 'ingenieur','lead': 'chef','full': 'developpeur','analyste': 'data analyst','product': 'chef de projet'}
    df["Intitulé du poste"] = df["Intitulé du poste"].apply(lambda x: ' '.join([terms_to_replace.get(term, term) for term in x.split()]))

    keywords = ["stage","business analyst","analyste fonctionnel","architecte","apprenti","data ingenieur","data ingénieur", "data engineer","data analyst","data scientist","consultant","ingenieur","chef de projet","concepteur","alternance",
                "technical leader","technicien","responsable","référent","expert","developpeur","specialiste","referent","manager","postdoctorant","internship"]

    for keyword in keywords:
        df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"(.*{keyword})", keyword, regex=True)
        df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"({keyword}.*)", keyword, regex=True)

    df['Intitulé du poste'] = df['Intitulé du poste'].apply(lambda x: re.sub(r'[hf]/[hf]|[-\/()]', '', x))

    return df


def clean_data_scrapping(df:pd.DataFrame) -> pd.DataFrame:

    ##### Salaires #####
    df[['Salaire minimum', 'Salaire maximum']] = df.loc[df['Salaires'].str.count('\d')>3,'Salaires'].str.extract(r'(\d+[,.]\d+|\d+).*?(\d+[,.]\d+|\d+)', expand=True)
    df[['Salaire minimum', 'Salaire maximum']] = df[['Salaire minimum', 'Salaire maximum']].apply(lambda x: x.str.replace(',', '.').astype(float))

    # les salaires avec k€ 
    df['Salaire minimum'] = df['Salaire minimum'].apply(lambda x: x*1000 if len(str(x).split(".")[0]) == 2 else x)
    df['Salaire maximum'] = df['Salaire maximum'].apply(lambda x: x*1000 if len(str(x).split(".")[0]) == 2 else x)
    # les salaires mensuels
    df['Salaire minimum'] = df['Salaire minimum'].apply(lambda x: x*12 if len(str(x).split(".")[0]) == 4 else x)
    df['Salaire maximum'] = df['Salaire maximum'].apply(lambda x: x*12 if len(str(x).split(".")[0]) == 4 else x)

    df['Salaire maximum'] = df['Salaire maximum'].apply(lambda x: None if x == 0 else x)

    ##### Type de contrat #####

    df['Type de contrat'] = df['Type de contrat'].apply(lambda x : str(x).split('-')[0].strip(' \u00a0\n\r').lower())

    ##### lieu #####

    df['lieu'] = df['lieu'].apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', x).strip().lower())

    ##### Intitulé de poste #####

    df['Intitulé du poste'] = df['Intitulé du poste'].apply(lambda x: re.sub(r'[hf]/[hf]|[-\/()]', '', x.lower()))
    keywords = ["stage","business analyst","analyste fonctionnel","architecte","apprenti","data ingenieur","data ingénieur", "data engineer","data analyst","data scientist","consultant","ingenieur","chef de projet","concepteur","alternance",
                    "technical leader","technicien","responsable","référent","expert","developpeur","specialiste","referent","manager","postdoctorant","internship",
                    "data protection officer","data privacy officer", "chargé de crm et data  marketing",
                    " product owner data média","data officer "]

    for keyword in keywords:
        df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"(.*{keyword})", keyword, regex=True)
        df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"({keyword}.*)", keyword, regex=True)

    ##### Date #####

    df['Date de publication'] = df['Date de publication'].apply(lambda x: datetime.strptime(x.strip(' \n\r').removeprefix('Actualisé le ').removeprefix('Publié le '), '%d %B %Y'))

    ##### Nom de la société #####

    df['Nom de la société'] = df['Nom de la société'].apply(lambda x : str(x).lower().strip(' \r\n'))

    ##### df dropna and drop 'Salaires' et colonne index duplicat #####
    df.drop('Salaires', axis=1, inplace=True)
    #df.dropna(how='any', inplace=True)

    return df


URL = "https://raw.githubusercontent.com/Lorenzo1208/Projet_TrouveTonJob/main/data.json"

DATASET_1 = clean_data_1(try_download_json(URL))
DATASET_2 = clean_data_scrapping(try_read_csv('https://raw.githubusercontent.com/Lorenzo1208/Projet_TrouveTonJob/main/data_scrapping.csv'))

df1 = pd.DataFrame(DATASET_1)
df2 = pd.DataFrame(DATASET_2)

df1['origine'] = "patrick"
df2['origine'] = "tarik"

DATASET_3 = pd.concat([df1, df2])


def get_dataset_1():

    return pd.DataFrame(DATASET_1)


def get_dataset_2():

    return pd.DataFrame(DATASET_2)


def get_dataset_3():

    return pd.DataFrame(DATASET_3)


def main():

    DATASET_1.to_csv("dataset_1.csv", index=False)
    DATASET_2.to_csv("dataset_2.csv", index=False)
    DATASET_3.to_csv("dataset_3.csv", index=False)


if __name__ == '__main__':
    main()