""" Importando as bibliotecas necessárias """

import streamlit as st
from inputs.form import FormDeem
from information.info import Table
from logout.Logoff import Logout
from Edition.Edit import Edits
from Initializer.Initializers import (
    InitializeFirebase,
    SetupPage,
    CheckLoginStatus,
    HandleLogin,
    DisplayMenu,
)


def main():
    """Função principal para executar o aplicativo Streamlit"""
    InitializeFirebase()
    SetupPage()
    CheckLoginStatus()

    if not st.session_state.logged_in:
        HandleLogin()
    else:
        option = DisplayMenu()
        if option == "Formulário de Deem":
            FormDeem()
        elif option == "Visão Geral":
            Table()
        elif option == "Editar Deem":
            Edits()
        elif option == "Sair":
            Logout()


if __name__ == "__main__":
    main()
