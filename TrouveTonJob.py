import string
import pandas as pd
import numpy as np
import requests
import unidecode
import re
import locale
from datetime import datetime
locale.setlocale(locale.LC_ALL,'fr_FR.UTF-8')
# Branch Tarik
def try_download_json(url:str) -> pd.DataFrame:

    try:
        response = requests.get(url)
        data = response.json()
        return pd.DataFrame(data)

    except:
        print(f"Erreur de chargement du lien - {url}")
        quit()


def clean_data(df:pd.DataFrame) -> pd.DataFrame:

    liste_salaires = df['lieu'].apply(lambda x : x[1] if len(x) > 1 else '')

    df['lieu'] = df['lieu'].apply(lambda x : unidecode.unidecode(x[0]))

    df['Nom de la société'] = df['Type de poste'].apply(lambda x : x[2] if len(x) > 2 else '')
    df['Type de contrat'] = df['Type de poste'].apply(lambda x : x[7].split(' - ')[0] if len(x) > 7 else '')
    df.drop(columns='Type de poste', inplace=True)

    df = df.apply(lambda c : c.apply(lambda x : ','.join([s.strip("\n ").lower() for s in (x.split(',') if type(x) != list else x)])))

    liste_dates = df['Date de publication'].apply(lambda x: '0 j' if x.find('heures') != -1 else x.removeprefix('postée il y a ').replace('postée hier', '1 j').strip('iorsu'))

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
    terms_to_replace = {'analyst': 'data analyst', 'datascientist': 'data scientist', 'data engineer': 'ingénieur','conultant/analyste': 'consultant/analyste','2018788': '',
                        'developer': 'developpeur','full stacke': 'developpeur','global technical seo manager': 'manager','engineer': 'ingenieur','lead': 'chef','full': 'developpeur','ingénieur': 'ingenieur','analyste': 'data analyst','product': 'chef de projet'}
    df["Intitulé du poste"] = df["Intitulé du poste"].apply(lambda x: ' '.join([terms_to_replace.get(term, term) for term in unidecode.unidecode(x).split()]))

    keywords = ["stage","business analyst","analyste fonctionnel","architecte","apprenti","data ingenieur","data ingénieur", "data engineer","data analyst","data scientist","consultant","ingenieur","chef de projet","concepteur","alternance",
                "technical leader","technicien","responsable","référent","expert","developpeur","specialiste","referent","manager","postdoctorant","internship"]

    for keyword in keywords:
        df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"(.*{keyword})", keyword, regex=True)
        df["Intitulé du poste"] = df["Intitulé du poste"].str.replace(rf"({keyword}.*)", keyword, regex=True)

    df['Intitulé du poste'] = df['Intitulé du poste'].apply(lambda x: re.sub(r'[hf]/[hf]|[-\/()]', '', x))

    return df

# Tarik lignes 66 à .... réservées au nettoyage du fichier data_scrapping.csv #########################################################

def try_read_csv(file) -> pd.DataFrame:

    try:
        df2 = pd.read_csv(file, index_col=0)
        return df2
    except:
        print(f"Erreur de lecture du csv - {file}")
        quit()

def clean_data_scrapping(df2:pd.DataFrame) -> pd.DataFrame:

    ############################## Salaires ##############################################################################################################################
    df2[['Salaire minimum', 'Salaire maximum']] = df2.loc[df2['Salaires'].str.count('\d')>3,'Salaires'].str.extract(r'(\d+[,.]\d+|\d+).*?(\d+[,.]\d+|\d+)', expand=True)


    df2[['Salaire minimum', 'Salaire maximum']] = df2[['Salaire minimum', 'Salaire maximum']].apply(lambda x: x.str.replace(',', '.').astype(float))
    # les salaires avec k€ 
    df2['Salaire minimum'] = df2['Salaire minimum'].apply(lambda x: x*1000 if len(str(x).split(".")[0]) == 2 else x)
    df2['Salaire maximum'] = df2['Salaire maximum'].apply(lambda x: x*1000 if len(str(x).split(".")[0]) == 2 else x)
    # les salaires mensuels
    df2['Salaire minimum'] = df2['Salaire minimum'].apply(lambda x: x*12 if len(str(x).split(".")[0]) == 4 else x)
    df2['Salaire maximum'] = df2['Salaire maximum'].apply(lambda x: x*12 if len(str(x).split(".")[0]) == 4 else x)

    #replace 0 with ''
    df2['Salaire maximum'] = df2['Salaire maximum'].apply(lambda x: None if x == 0 else x)

    ###########################   Type de contrat   ##########################################################################################################################################

    df2['Type de contrat'] = df2['Type de contrat'].apply(lambda x : str(x).split('-')[0].lower())

    ###########################   lieu   ##########################################################################################################################################

    df2['lieu'] = df2['lieu'].apply(lambda x: re.sub(r'[^a-zA-Z]', ' ', x).strip().lower())

    ###########################   Intitulé de poste   ##########################################################################################################################################

    df2['Intitulé du poste'] = df2['Intitulé du poste'].apply(lambda x: re.sub(r'[hf]/[hf]|[-\/()]', '', x.lower()))
    keywords = ["stage","business analyst","analyste fonctionnel","architecte","apprenti","data ingenieur","data ingénieur", "data engineer","data analyst","data scientist","consultant","ingenieur","chef de projet","concepteur","alternance",
                    "technical leader","technicien","responsable","référent","expert","developpeur","specialiste","referent","manager","postdoctorant","internship",
                    "data protection officer","data privacy officer", "chargé de crm et data  marketing",
                    " product owner data média","data officer "]

    for keyword in keywords:
        df2["Intitulé du poste"] = df2["Intitulé du poste"].str.replace(rf"(.*{keyword})", keyword, regex=True)
        df2["Intitulé du poste"] = df2["Intitulé du poste"].str.replace(rf"({keyword}.*)", keyword, regex=True)

    ########################## Date ################################################################################################

    df2['Date de publication'] = df2['Date de publication'].str.replace('Actualisé le', '').str.replace('Publié le', '')
    df2['Date de publication'] = df2['Date de publication'].apply(lambda x: datetime.strptime(x.strip(),'%d %B %Y').strftime("%Y-%m-%d"))

    ########################### Nom de la société ################################################################################

    df2['Nom de la société'] = df2['Nom de la société'].str.lower()

    ########################## df2 dropna and drop 'Salaires' et colonne index duplicat ##############################################
    df2.drop('Salaires', axis=1, inplace=True)
    df2.dropna(how='any', inplace=True)

    return df2




def main():

    url = "https://raw.githubusercontent.com/Lorenzo1208/Projet_TrouveTonJob/main/data.json"

    df = try_download_json(url)
    df = clean_data(df)

    df2 = try_read_csv('data_scrapping.csv')
    df2 = clean_data_scrapping(df2)
    # jeu de données final df1+df2
    df = df.dropna().reset_index(drop=True)
    
    # Imputation à faire sur Type de poste et lieu en prenant la valeur qui revient le plus
    df3 = pd.concat([df,df2],axis=0)
    # Imputation Type de contrat fillna with cdi et lieu with paris
    df3['Type de contrat'] = df3['Type de contrat'].replace('',np.nan,regex=True)
    df3['Type de contrat'] = df3['Type de contrat'].replace(np.nan,'cdi',regex=True) # Remplace le blank avec nan
    # df3['Type de contrat'] = df3['Type de contrat'].fillna("cdi")
    df3['lieu'] = df3['lieu'].replace('',"paris",regex=True) # Remplace le blank avec nan
    
    df3 = df3.reset_index(drop=True)
    print(df2.shape)
    df.to_csv("data_clean.csv", index=False)
    df2.to_csv("data_scrapping_clean.csv", index=False)
    df3.to_csv("data_finale_clean.csv", index=False)
if __name__ == '__main__':
    main()