import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from inputs.form import FormDeem

# Inicializando o serviço do banco de dados Firebase:

try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)

database = firestore.client()


def app():

    option = st.sidebar.radio(
        "Menu de navegação", options=["Formulário de Deem 🗒️", "Recarregar 🔃"]
    )

    if option == "Formulário de Deem 🗒️":
        FormDeem()
    if option == "Recarregar 🔃":
        pass


if __name__ == "__main__":
    app()
