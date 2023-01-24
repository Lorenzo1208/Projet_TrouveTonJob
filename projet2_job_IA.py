# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 14:36:19 2023

@author: tarik
"""

#import libraries
import pandas as pd
import numpy as np
import json
import re
from datetime import timedelta


#read json


# Opening JSON file
f = open('data.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

# Iterating through the json
# list

pd.io.json.json_normalize(data)

#Type de contrat
data[0]['Type de poste'][7]

#Nom entreprise
data[0]['Type de poste'][2]

#Type entreprise
data[0]['Type de poste'][4]

# compétences
data[0]['competences']

#Salaire
data[5]['lieu'][1]


print(type(data[0]['competences']))

df = pd.DataFrame([{'Date de scrapping': pd.to_datetime('2023-01-15').strftime("%Y-%m-%d"),'Date de publication': i['Date de publication'] ,'Intitulé de poste': i['Intitulé du poste'][0].lower(), 'Type de contrat': i['Type de poste'][7] if len(i['Type de poste']) > 7 else '', 'Nom entreprise': i['Type de poste'][2] if len(i['Type de poste']) > 2 else '',
      'Type entreprise': i['Type de poste'][4] if len(i['Type de poste']) > 4 else '', 'compétences': i['competences'], 'Salaire': i['lieu'][1] if len(i['lieu']) > 1 else '' }for i in data ])
print(df)


#colonne compétence remplace le \n par rien
df['compétences'] = df['compétences'].apply(lambda x: [i.replace('\n', '') for i in x])

######################### La colonne 'Intitulé de poste' #######################################################################################################################################################################

#remplace si data analyst dans vavlue par data analyste etc
df['Intitulé de poste'] = df['Intitulé de poste'].apply(lambda x: x.replace(x,'data analyst') if 'data analyst ' in x else x.replace(x,'data scientist ') if 'data scientist' in x else x.replace(x,'data engineer') if 'data engineer' in x else x )
 
# Remplace les characters 'h/f' or 'f/h' or '(h/f)' with '' in colunne 'Intitulé de poste'
df['Intitulé de poste'] = df['Intitulé de poste'].apply(lambda x: re.sub(r'[hf]\/[hf]|\([hf]\/[hf]\)', '', x))

#Remplace les valeur numérique par rien
df['Intitulé de poste'] = df['Intitulé de poste'].apply(lambda x: re.sub(r'\d+', '', x))

# création d'une liste de termes à suprimer comme des stopword
remove_list = ['alterance', '#']
# Suppression de ces derniers dans la colonne 

df['Intitulé de poste'].replace(remove_list, '', inplace=True, regex=True)


#date parution



df['Date de publication'] = df['Date de publication'].apply(lambda x: x.replace(x,'postée il y a 1 jours') if 'postée hier' in x else x)
df['Date de publication'] = df['Date de publication'].apply(lambda x: x.replace('postée il y a ',''))



def subtract_days_from_date(date, days):
    """Subtract days from a date and return the date.
    
    Args: 
        date (string): Date string in YYYY-MM-DD format. 
        days (int): Number of days to subtract from date
    
    Returns: 
        date (date): Date in YYYY-MM-DD with X days subtracted. 
    """
    
    subtracted_date = pd.to_datetime(date) - timedelta(days=days)
    subtracted_date = subtracted_date.strftime("%Y-%m-%d")

    return subtracted_date

def subtract_months_from_date(date, months):
    """Subtract months from a date and return the date.
    
    Args: 
        date (string): Date string in YYYY-MM-DD format. 
        months (int): Number of months to subtract from date
    
    Returns: 
        date (date): Date in YYYY-MM-DD with X months subtracted. 
    """
    
    subtracted_date = pd.to_datetime(date) - pd.DateOffset(months=months)
    subtracted_date = subtracted_date.strftime("%Y-%m-%d")

    return subtracted_date




def calculate_date(row, date_col, delta_col):
    # Extract the number of days or months from the delta column
    if 'jour' in row[delta_col]:
        delta = int(row[delta_col].split()[0])
        delta_unit = 'days'
    elif 'mois' in row[delta_col]:
        delta = int(row[delta_col].split()[0])
        delta_unit = 'months'
    else:
        return row[date_col]
    if delta_unit == 'days':
        new_date = subtract_days_from_date(row[date_col],delta)
    else:
        new_date = subtract_months_from_date(row[date_col],delta)
    return new_date

# Apply the function to the dataframe
df['date_paru'] = df.apply(calculate_date, args=('Date de scrapping', 'Date de publication'), axis=1)







#split les valeurs séparées par un - et garde la première partie
df['Intitulé de poste'] = df['Intitulé de poste'].apply(lambda x: x.split("-")[0])
 
# Closing file
f.close()


# converting the data to dataframe
df_job = pd.json_normalize(data,max_level=5)