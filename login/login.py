import streamlit as st
from firebase_admin import auth
import pyrebase


# Configuração do Firebase:


config = {
    "apiKey": "AIzaSyDJnEKvU9-yJSlTqGT3O9as2paIzJFNBts",
    "authDomain": "deem-fa6c8.firebaseapp.com",
    "databaseURL": "https://deem-fa6c8-default-rtdb.firebaseio.com",
    "projectId": "deem-fa6c8",
    "storageBucket": "deem-fa6c8.appspot.com",
    "messagingSenderId": "165164284179",
    "appId": "1:165164284179:web:c9b6e99c834dffb08702e6",
}

# Inicializando e autenticando o aplicativo:


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


# Função para verificar se o usuário e senha inseridas existem no banco de dados Firebase:


def Login():

    st.title("Gerenciamento de Deem's - Login")
    email = st.text_input("E-mail", key="input_email")
    password = st.text_input("Senha", key="input_password", type="password")

    if st.button("Entrar"):
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            st.success("Login bem-sucedido!")
            return user["localId"]  # Retornando o identificador do usuário
        except:
            st.error(
                "Usuário ou senha incorretos, verifique as informações inseridas e se o erro persistir entre em contato com seu gestor."
            )
            return None
