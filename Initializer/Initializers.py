""" Importando as bibliotecas necessárias """

import streamlit as st
import firebase_admin
from firebase_admin import credentials
from streamlit_option_menu import option_menu
from Authentication.login import Login


"""Variáveis"""
Credentials_path = "credentials.json"
Page_title = "Controle de Deem"
Menu_option = ["Formulário de Deem", "Visão Geral", "Editar Deem", "Sair"]
Menu_icons = ["journal-text", "table", "pencil-square", "door-closed"]


def InitializeFirebase():
    """Inicializar o Firebase usando um arquivo de credenciais JSON"""
    try:
        firebase_admin.get_app()
    except ValueError:
        cred = credentials.Certificate(Credentials_path)
        firebase_admin.initialize_app(cred)


def SetupPage():
    """Define corretamente o título da página."""
    st.set_page_config(page_title=Page_title)


def CheckLoginStatus():
    """Verifica se o usuário está logado usando a variável de estado da sessão do Streamlit (st.session_state)"""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False


def HandleLogin():
    """Gerenciando o processo de login do usuário no seu aplicativo Streamlit"""
    user = Login()
    if user:
        st.session_state.logged_in = True
        st.session_state.user_id = user
        st.rerun()


def DisplayMenu():
    """Exibi opções de menu na barra lateral com ícones correspondentes"""
    with st.sidebar:
        option = option_menu(
            menu_title="Menu de navegação",
            options=Menu_option,
            icons=Menu_icons,
            default_index=0,
        )
    return option
