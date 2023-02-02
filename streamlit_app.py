from pathlib import Path
import streamlit as st
from st_pages import Page, add_page_title, show_pages
st.set_page_config(layout="wide")
# with open("assets/style.css") as style:
#     st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)

show_pages(
        [
            
            Page("streamlit_app.py", "Le Projet", ""),
            # Can use :<icon-name>: or the actual icon
            Page("streamlit_pages/data_profiling_page.py", "Data Profiling", ""),
            # The pages appear in the order you pass them
            # Page("streamlit_pages/nettoyage_page.py", "Nettoyage", ""),
            Page("streamlit_pages/analyse_page.py", "Analyse descriptive et exploratoire", ""),
            # Will streamlit_pagesuse the default icon and name based on the filename if you don't
            # pass them
            Page("streamlit_pages/modelisation_page.py","Modélisation en Machine learning")
        ]
    )

st.image("https://github.com/Lorenzo1208/Projet_TrouveTonJob/blob/main/assets/Logo.png?raw=true", width=400)



st.markdown('''
<style>
[data-testid="stMarkdownContainer"] ul{
    padding-left:40px;
}
</style>
''', unsafe_allow_html=True)
context_projet_html_string = f'''
<h1>Trouve ton job dans l'IA</h1>
<h2>Bienvenue sur TrouveTonJob ! </h2>
<h2>Contexte du projet:</h2>
<div><p class="sc-6a4c5dd9-0 krAuxe">En tant que futur développeur IA vous allez vous familiariser avec le marché de l'emploi du secteur.</p>
<p class="sc-6a4c5dd9-0 krAuxe">A partir d'un jeu de données fourni (issu du web scraping), vous allez réaliser le/la :</p>
<ul class="sc-6a4c5dd9-0 sc-99b17411-0 cJZwRL GeZKg">
<li>Intégration des données</li>
<li>Nettoyage</li>
<li>Préparation</li>
<li>Analyse descriptive et exploratoire</li>
<li>Modélisation grâce au machine learning</li>
<li>Développement d'une application web</li>
</ul>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">Les données correspondent à des offrent en Ile de France uniquement.</p>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">Après avoir intégrer les données vous ferez en sorte d'avoir au moins les colonnes suivantes :</p>
<ul class="sc-6a4c5dd9-0 sc-99b17411-0 cJZwRL GeZKg">
<li>Date de publication : Le format doit être <b>AAAA-MM-JJ</b>, contrairement à ce que vous avez dans les données qui est un nombre de jour correspondant au nombre de jour(s) écoulé(s) depuis l'annonce. Vous prendrez comme base le 15/01/2023. Prenons l'exemple d'une annonnce qui a 22 jours. Si nous sommes le 23 janvier, vous devrez donc ajouter 8 jours (Du 15 janvier au 23 cela fait 8 jours), ce qui fera 30 jours depuis la mise en ligne de l'annonce. La valeur de la colonne <b>Date de publication <b>pour l'annonce sera donc</b> 24/12/2022 (30 jours plus tôt). N'oubliez pas de mettre la colonne au format date.</b></li>
<li>Intitulé du poste : Une colonne qui contient** l'intitulé du poste en minuscule, et uniquement cela.** En effet certaines lignes contiennent aussi les <b>noms des entreprises</b> ou la mention **F/H **qui est à supprimer également. La ligne ne doit contenir que l'intitulié du poste. Ce qui permettra de faire un comptage du nombre de fois qu'un intitulé de poste précis apparait.</li>
<li>competences : La liste des compétences séparées par une virgule &gt; **scala, data quality, edge, python, big data	**</li>
<li>lieu : Les lieux en minuscule. Attention de bien vérifier qu'il y a une uniformité des noms. Vous devrez donc nettoyer pour faire un choix entre **Ile de France, Ile-de-France ou Île-de-France **par exemple, qui correspondent au même endroit.</li>
<li>Salaire : Vous devez splitter les données en deux colonnes, une colonne <b>salaire_minimum</b> et une <b>salaire_maximum</b>.</li>
<li>Type de contrat : Vous ne conserverez que le type de contrat. Donc uniquement <b>CDI</b> et non pas <b>CDI - temps plein</b>.</li>
<li>Nom de la société : Vous les indiquerez en minuscule. Attention de bien vérifier qu'il y a une uniformité des noms.</li>
</ul>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">Voici quelques exemples d'analyses que vous pouvez effectuer :</p>
<ul class="sc-6a4c5dd9-0 sc-99b17411-0 cJZwRL GeZKg">
<li>Les compétences les plus recherchées</li>
<li>Les entreprises qui recrutent le plus</li>
<li>Les postes les mieux payés</li>
<li>Les compétences les mieux payés</li>
<li>Le salaire moyen par compétence</li>
<li>Les types de contrat</li>
</ul>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">Vous ferez une analyse multivariée. Par exemple y a t'il un lien entre les compétences et le type de contrat ? Par quoi est influencé le salaire ? Est-ce que certaines compétences sont surtout liés à certains types de poste, ou d'entreprises ?</p>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">Enfin pour la partie machine learning, vous essayerez de prédire :</p>
<ul class="sc-6a4c5dd9-0 sc-99b17411-0 cJZwRL GeZKg">
<li>Le salaire minimum et maximum en utilisant la méthode de votre choix</li>
<li>Vous ferez du clustering en utilisant un maximum de données pour regrouper les offres entre elle. Que remarquez vous ? Caractérisez les clusters en analysant leur statistiques. Vous justifierez votre choix du nombre de cluster.</li>
</ul>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">Pour finir, vous ferez une application web sur laquelle une personne pourra visualiser vos résultats. Il s'agira donc de graphiques interactifs à l'attention d'une personne voulant se faire une idée du marché de la Data en Ile de France.</p>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">Il faudra qu'un utilisateur puisse indiquer** son intitulé de poste et quelques compétences,** et le modèle que vous aurez développé devra indiquer <b>un salaire minimum et maximum</b> auquel il pourra prétendre, et **recommandera des entreprises qui seraient susceptibles de l'embaucher. **</p>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>
<p class="sc-6a4c5dd9-0 krAuxe">​</p>


</div>
<div class="sc-f06a72bb-0 euZDmQ">
<h2 class="sc-6a4c5dd9-0 cTzoBk">Modalités pédagogiques</h2>
<div>
<div>
<p class="sc-6a4c5dd9-0 krAuxe">Projet à réaliser en 3 semaines.</p>
<p class="sc-6a4c5dd9-0 krAuxe">Equipe projet de 3 personnes, constituée aléatoirement</p>
</div>
</div>
</div>
<div class="sc-f06a72bb-0 euZDmQ">
<h2 class="sc-6a4c5dd9-0 cTzoBk">Critères de performance</h2>
<div>
<div>
<p class="sc-6a4c5dd9-0 krAuxe">L'application web est fonctionnelle et elle répond aux attentes du projet :</p>
<ul class="sc-6a4c5dd9-0 sc-99b17411-0 cJZwRL GeZKg">
<li>Intégration de plusieurs composants d'interaction</li>
<li>Restitution d'éléments descriptifs et explicatifs du marché de l'emploi</li>
<li>Restitution des résultats et prédictions du/des modèles de machine learning développé(s).</li>
</ul>
</div>
</div>
</div>
<div class="sc-f06a72bb-0 euZDmQ">
<h2 class="sc-6a4c5dd9-0 cTzoBk">Modalités d'évaluation</h2>
<div>
<div>
<p class="sc-6a4c5dd9-0 krAuxe">Evaluation par un jury : formateur + pairs
Soutenance par groupe :</p>
<ul class="sc-6a4c5dd9-0 sc-99b17411-0 cJZwRL GeZKg">
<li>15 minutes pour présenter le travail réalisé et faire un démonstration de l'application</li>
<li>5 minutes de Q/A</li>
</ul>
</div>
</div>
</div>

<div class="sc-f06a72bb-0 euZDmQ">
<h2 class="sc-6a4c5dd9-0 cTzoBk">Livrables</h2><p class="sc-6a4c5dd9-0 krAuxe">
- Une application web qui permet d'interagir avec les données et les prédictions du/des modèles de machine learning développé(s).
- Une présentation écrite et orale résumant vos travaux.
- Un dépôt Github.
- Trello du projet
- Bonus :
* gestion des erreurs,
* enrichissement des données (sources complémentaires à identifier),
* multiples fonctionnalités supplémentaires,
* analyse de données avancée,
* mise en œuvre de plusieurs concepts d’apprentissage supervisé et non supervisé,
* etc.</p>
<p class="sc-6a4c5dd9-0 krAuxe"><h2><b>Yapluka !</b></h2></p>
</div>
'''
st.markdown(context_projet_html_string, unsafe_allow_html=True)
    



