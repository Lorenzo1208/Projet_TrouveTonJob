import pandas as pd

def dix_competences_plus_recherchees(input_dataframe):
    if input_dataframe == "df1":
        dix_competences_plus_recherchees = df1["competences"].str.split(",", expand=True).stack().str.strip().value_counts()
        return dix_competences_plus_recherchees.head(10)
    else:
        dix_competences_plus_recherchees = df3["competences"].str.split(",", expand=True).stack().str.strip().value_counts()
        return dix_competences_plus_recherchees.head(10)

def dix_entreprise_recrute_plus(input_dataframe):
    if input_dataframe == "df1":
        dix_entreprise_recrute_plus = df1["Nom de la société"].str.split(",", expand=True).stack().str.strip().value_counts()
        return dix_entreprise_recrute_plus.head(10)
    else:
        dix_entreprise_recrute_plus = df3["Nom de la société"].str.split(",", expand=True).stack().str.strip().value_counts()
        return dix_entreprise_recrute_plus.head(10)

def dix_poste_mieux_paye(input_dataframe):
    if input_dataframe == "df1":
        df1["Salaire_moyen"] = (df1['Salaire minimum'] + df1['Salaire maximum']) / 2
        dix_poste_mieux_paye = df1.groupby("Intitulé du poste").mean(numeric_only=True).sort_values("Salaire_moyen", ascending=False)
        return dix_poste_mieux_paye.head(10)
    else:
        df3["Salaire_moyen"] = (df3['Salaire minimum'] + df3['Salaire maximum']) / 2
        dix_poste_mieux_paye = df3.groupby("Intitulé du poste").mean(numeric_only=True).sort_values("Salaire_moyen", ascending=False)
        return dix_poste_mieux_paye.head(10)
    
def types_contrat(input_dataframe):
    if input_dataframe == "df1":
        types_contrat = df1["Type de contrat"].str.split(",", expand=True).stack().str.strip().value_counts()
        return types_contrat
    else:
        types_contrat = df3["Type de contrat"].str.split(",", expand=True).stack().str.strip().value_counts()
        return types_contrat
    
def competences_mieux_payees(input_dataframe):
    if input_dataframe == "df1":
        df1["Salaire_moyen"] = (df1['Salaire minimum'] + df1['Salaire maximum']) / 2
        competences_mieux_payees = df1.groupby(["competences"]).mean().sort_values("Salaire_moyen", ascending=False)
        return competences_mieux_payees.head(10)
    else :
        df3["Salaire_moyen"] = (df3['Salaire minimum'] + df3['Salaire maximum']) / 2
        competences_mieux_payees = df3.groupby(["competences"]).mean().sort_values("Salaire_moyen", ascending=False)
        return competences_mieux_payees.head(10)

def salaire_moyen_par_competences(input_dataframe):
    if input_dataframe == "df1":
        df1["Salaire_moyen"] = (df1['Salaire minimum'] + df1['Salaire maximum']) / 2
        salaire_moyen_par_competences = df1[["competences", "Salaire_moyen"]].dropna()
        salaire_moyen_par_competences["competences"] = salaire_moyen_par_competences["competences"].str.split(",")
        salaire_moyen_par_competences = salaire_moyen_par_competences.explode("competences")
        salaire_moyen_par_competences = salaire_moyen_par_competences.groupby("competences").mean()
        return salaire_moyen_par_competences.head(10)
    else :
        df3["Salaire_moyen"] = (df3['Salaire minimum'] + df3['Salaire maximum']) / 2
        salaire_moyen_par_competences = df3[["competences", "Salaire_moyen"]].dropna()
        salaire_moyen_par_competences["competences"] = salaire_moyen_par_competences["competences"].str.split(",")
        salaire_moyen_par_competences = salaire_moyen_par_competences.explode("competences")
        salaire_moyen_par_competences = salaire_moyen_par_competences.groupby("competences").mean()
        return salaire_moyen_par_competences.head(10)

def affiche(input_print):
    if input_print == "10comp":
        print(dix_competences_plus_recherchees(input_dataframe))
    elif input_print == "10entr":
        print(dix_entreprise_recrute_plus(input_dataframe))
    elif input_print == "10post":
        print(dix_poste_mieux_paye(input_dataframe))
    elif input_print == "types":
        print(types_contrat(input_dataframe))
    elif input_print == "comp":
        print(competences_mieux_payees(input_dataframe))
    elif input_print == "salaire":
        print(salaire_moyen_par_competences(input_dataframe))

def main():
    global input_dataframe
    global input_print
    print("Bonjour, bienvenue dans notre programme de recherche d'emploi !")
    input_dataframe = input("Quel dataset voulez-vous utiliser ? df1 (dataset1 données Patrick) ou df3 (dataset3 données Tarik) ?\n")
    input_print = input("Print 10comp (10compétences plus recherchées)  10entr (dix_entreprise_recrute_plus)  10post (dix_poste_mieux_paye)  types (types_contrat) comp ( competences_mieux_payees) salaire (salaire_moyen_par_competences) ?\n")
    affiche(input_print)
    
df1 = pd.read_csv('dataset_1.csv', index_col=0)
df3 = pd.read_csv('dataset_3.csv', index_col=0)

main()
