import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from inputs.form import FormDeem
from streamlit_option_menu import option_menu
from information.info import Table
from login.login import Login
from logout.logoff import logout

# Inicializando o serviço do banco de dados Firebase:
try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)

database = firestore.client()

st.set_page_config(page_title="Controle de Deem")


def app():

    # Garante que sempre teremos um estado inicial de não logado:

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # Verificamos se o usuário está logado:

    if not st.session_state.logged_in:
        user = Login()
        if user:
            st.session_state.logged_in = True
            st.session_state.user_id = user
            st.rerun()
    else:
        with st.sidebar:
            option = option_menu(
                menu_title="Menu de navegação",
                options=["Formulário de Deem", "Visão Geral", "Recarregar", "Sair"],
                icons=[
                    "journal-text",
                    "bar-chart-fill",
                    "arrow-clockwise",
                    "door-closed",
                ],
                default_index=0,
            )

        if option == "Formulário de Deem":
            FormDeem()
        if option == "Visão Geral":
            Table()
        if option == "Recarregar":
            pass
        if option == "Sair":
            logout()


if __name__ == "__main__":
    app()
