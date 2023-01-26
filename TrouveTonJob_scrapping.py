# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 14:34:44 2023

@author: tarik
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from requests import get
from requests.exceptions import RequestException
from contextlib import closing

from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time

start_time = time.time()

#try:
region='11R'
keyword='Data+analyste'
#except:
#    region='11R' ile de france
#    keyword='Data+analyste'

print("Région: "+region+", kwd: "+keyword)

#Demander le(s) mot(s) clés & et le(s) lieu(x)
query = input("Veuillez enter le(s) mot(s) clés pour la recherche: \n").lower()
location = input("Veuillez enter le(s) lieu(x) pour la recherche: \n").upper()


#launch url
url = "https://candidat.pole-emploi.fr/offres/recherche?lieux={}&motsCles={}&offresPartenaires=true&range=0-9&rayon=10&salaireMin=20000&tri=0&typeContrat=CDI,CDD&uniteSalaire=A&uniteSalaire=A".format(location,query)

#set webdriver path
driver = webdriver.Firefox(executable_path ='geckodriver')

# fonction connection



def simple_get(url):
    """
    Se connecte a l'url, si statut = 200 retourne le contenu ( en appelant is_good_response)
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None
def is_good_response(resp):
    """
    Renvoie 200 si connection a l'url
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)
def log_error(e):
    """
    retourne l'erreur
    """
    print(e)




# create a new Firefox session

driver.implicitly_wait(10)

#driver.implicitly_wait(10)
driver.get(url)

cookie_button = driver.find_element("id",'footer_tc_privacy_button_2') #click sur accepter les coockies
cookie_button.click() #click accepter les coockies



time.sleep(5)
job1_button = driver.find_element("id",'pagelink_0')
job1_button.click() #click sur le premier lien de job ouvre le pop-up

#Récuperer la soupe
#Selenium hands the page source to Beautiful Soup
soup=BeautifulSoup(driver.page_source, 'lxml')
##printing soup in a more structured tree format that makes for easier reading


#recuperer le nombre d'offres
nombre_offres = int(soup.find("span", {"class": "nb-total"}).get_text())
print("il ya ",nombre_offres,"Offres pour votre recherche")

# Creating an empty Dataframe with column names only
dfObj = pd.DataFrame(columns=['Titre de l\'offre', 'Localisation', 'Experiences'])	

#Definission des listes

title=[]
Localisation=[]
Publication=[]
Salaires=[]
Entreprises=[]
Type_contrat=[]
Competences=[]
# Create a list of skills to check for
skills_to_check = ["python", "sql", "agile",'test','big data','recette','outils'
                   ,'communication','intelligence artificielle','nosql','hadoop',
                   'marketing','iaas','paas','saas',
                   'electronique','validation','data management',
                   'business intelligence','machine learning','plm',
                   'git','bases de données','support','java','decisionnel','t-sql',
                   'scrum','réseaux sociaux','réseaux','acquisition','jquery',
                   'sas','sap','windows','power bi','scala','unix',
                   'bootstrap','web','sql server','oracle','mysql','postgresql',
                   'spring','téléphonie','serveur','cloud','qlik','tableau',
                   'network','moe','moa','c++','c#','vmware','linux','unix',
                   'android','devops','qlikview','sécurité','php','php5',
                   'javascript','angularjs','symfony',
                   'jenkins','seo','vba','excel','j2ee','salesforce','ios',
                   'data quality','cognos','talend','etl','crm','spark','npl',
                   'nlp','tensorflow','keras']
for i in range(1, nombre_offres+1):
    
    print("------------",i,"---------")
       
    soup = BeautifulSoup(simple_get(driver.current_url), 'html.parser')
    #print(soup.prettify())
    #print("end soup",i)
    try:
        Titre=soup.find(itemprop = "title").get_text()
        print(Titre)
        title.append(Titre)
    except:
        title.append("")
        print("il ya pas de titre")
    try:
        Where=soup.find("span", {"itemprop": "name"}).get_text()
        print(Where)
        Localisation.append(Where)
    except:
        Localisation.append("")
        print("il ya pas de localisation")
    
    try:
        Date_pub=soup.find("span", {"itemprop": "datePosted"}).get_text()
        print(Date_pub)
        Publication.append(Date_pub)
    except:
        Publication.append("")
        print("il ya pas de date de publication")
    
    try:
        Salaire=soup.find("ul", {"style": "list-style-type: none; margin:0; padding: 0"}).find("li").get_text()
        print(Salaire)
        Salaires.append(Salaire)
    except:
        Salaires.append("")
        print("il ya pas de date de salaire")
        
    try:
        entreprise=soup.find("div", {"class": "media-body"}).find("h3",{"class":"t4 title"}).get_text()
        print(entreprise)
        Entreprises.append(entreprise)
    except:
        Entreprises.append("")
        print("il ya pas de date d'entreprise") 
        
    try:
        contrat=soup.find("p", {"class": "contrat"}).get_text()
        print(contrat)
        Type_contrat.append(contrat)
    except:
        Type_contrat.append("")
        print("il ya pas de type de contrat") 
        
    try:
        job_offer=soup.find("div", {"itemprop": "description"}).find("p").get_text()
        # Extract the text of the job offer
        offer_text = job_offer.lower()
        skills_found = []
        # Iterate over the skills to check for
        for skill in skills_to_check:
            if skill in offer_text:
                skills_found.append(skill)
        if skills_found:
            Competences.append(", ".join(skills_found))
        else:
            Competences.append("")
        print(offer_text)
    except:
        Competences.append("")
        print("il ya pas de type de compétences") 

    #pause
    #time.sleep(4)
        #click sur suivant
    suivant_button = driver.find_element("xpath",'//*[@title="Suivant"]')
    suivant_button.click() #click sur le premier lien de job ouvre le pop-up
#    driver.implicitly_wait(60)
    
df = pd.DataFrame({"Intitulé du poste":title,
                   "Date de publication" : Publication,"lieu":Localisation,"competences":Competences,
                   "Nom de la société":Entreprises,"Type de contrat":Type_contrat,
                   "Salaires":Salaires})
print(df)
df.to_csv("data_scrapping.csv", encoding="utf-8")   




driver. quit()   
          
from datetime import datetime
# current date and time
now = datetime.now()
timestamp = datetime.timestamp(now)
print("timestamp =", timestamp)
print(now)
print("il ya ",nombre_offres,"Offres pour votre recherche")
print("--- %s seconds ---" % (time.time() - start_time))