import string
import pandas as pd
import numpy as np
import requests
import unidecode
import re


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
        df2 = pd.read_csv(file)
        return df2

    except:
        print(f"Erreur de lecture du csv - {file}")
        quit()

def clean_data_scrapping(df2:pd.DataFrame) -> pd.DataFrame:

    # Check if salary is in monthly, if yes, multiply by 12
    df2['Salaires'] = df2['Salaires'].apply(lambda x: x['Salaires'].replace("Mensuel de ", "").replace(" Euros à "," - ").replace(" Euros sur 12 mois", "") if 'Mensuel' in x['Salaires'] else x['Salaires'], axis=1)

    # Extract minimum and maximum salary values
    df2[['salary_min', 'salary_max']] = df2['Salaires'].str.extract('(?P<salary_min>\d+[.,]?\d+)[ -]+(?P<salary_max>\d+[.,]?\d+)', expand=True)

    # convert columns to numeric
    df2[['salary_min', 'salary_max']] = df2[['salary_min', 'salary_max']].apply(pd.to_numeric)

    # multiply by 12 if salary is monthly
    df2[['salary_min', 'salary_max']] = df2.apply(lambda x: x[['salary_min', 'salary_max']]*12 if 'Mensuel' in x['Salaires'] else x[['salary_min', 'salary_max']], axis=1)

    # Replace NaN values with None
    df2.replace(np.nan, '', inplace=True)

    # Replace non-numeric values with None
    df2.replace(r'[^\d.,]+', '', regex=True, inplace=True)

    

    return df2




def main():

    url = "https://raw.githubusercontent.com/Lorenzo1208/Projet_TrouveTonJob/main/data.json"

    df = try_download_json(url)
    df = clean_data(df)

    df2 = try_read_csv('data_scrapping.csv')
    df2 = clean_data_scrapping(df2)

    df.to_csv("data_clean.csv")
    df2.to_csv("data_scrapping_clean.csv")

if __name__ == '__main__':
    main()