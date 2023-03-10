import streamlit as st
import datetime
import pandas as pd
import pickle
import numpy as np
import modelisation
from st_pages import add_page_title
from streamlit_extras.colored_header import colored_header

st.set_page_config(layout="wide")
with open("assets/style.css") as style:
    st.markdown(f"<style>{style.read()}</style>", unsafe_allow_html=True)
    from streamlit_extras.let_it_rain import rain
    st.title("Modélisation avec le machine learning 🤖")
    colored_header(
        label="",
        description="",
        color_name="green-70",
    )
    st.title("Estimer votre salaire 🤑")
    with st.expander("Pipeline du modèle 🔍"):
        st.image("https://github.com/Lorenzo1208/Projet_TrouveTonJob/blob/main/assets/pipe.png?raw=true")

    def on_submit_click(**kwargs):
        resp = send_update(**kwargs)
        st.success('Task submitted')

    with st.form('Prédiction', clear_on_submit=True):
        job= st.text_input("Job recherché")
        skills= st.text_input("Vos compétences")
        entreprises= st.text_input("Entreprises recherchés")
        lieu= st.text_input("Lieu de votre recherche")
        contrat= st.text_input("Pour quel type de contrat")
        date= st.date_input("Date de disponibilité",datetime.datetime.now())


        submitted = st.form_submit_button('Estimez votre salaire')
        if submitted:
            data_input={'Intitulé du poste':[job], 'competences':[skills], 'Nom de la société':[entreprises],
                                'lieu':[lieu], 'Type de contrat':[contrat],
                                'Date de publication':date}
            df_input = pd.DataFrame.from_dict(data_input)

            df_input = df_input.applymap(lambda x: x.replace(', ', ' ').replace(',', ' ') if isinstance(x, str) else x)
                # Find the minimum date
            min_date = df_input ['Date de publication'].min()

                # Create a new column 'Encoded_date' by subtracting the minimum date from the original date column
            df_input ['Date de publication'] = (df_input ['Date de publication'] - min_date).dt.days
                # df_input['Date de publication'] = df_input["Date de publication"].apply(lambda x: x.timestamp())
            st.write(df_input)



                # load the model from disk
            model = pickle.load(open('model_test.model', 'rb'))

            y = model.predict(df_input)
            y_max = int(y[0][1])
            y_min = int(y[0][0])
            if y_max < y_min:
                y_min= int(y[0][1])
                y_max = int(y[0][0])
            else:
                y_min= int(y[0][0])
                y_max = int(y[0][1])
                col1, col2 = st.columns(2)
                col1.metric(label="Salaire minimum", value=f"{y_min} en €/an 💶")
                col2.metric(label="Salaire maximum", value=f"{y_max} en €/an 💵")
                # style_metric_cards()
                # st.write(f"Votre salaire est entre: {y_min} et {y_max} en €/an")
            rain(
            emoji="💸",
            font_size=54,
            falling_speed=5,
            animation_length="infinite",
        )
                

    with st.sidebar: 
        st.image("https://www.onepointltd.com/wp-content/uploads/2020/03/inno2.png")
        st.title("Estimer votre salaire 🤑")
        choice = st.radio("Navigation", ["Modélisation"])
        st.info("Cette section vous permet d'estimer votre salaire !")
