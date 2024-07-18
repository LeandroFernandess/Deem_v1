import streamlit as st
from firebase_admin import auth
import pyrebase

# Configuração do Firebase:
config = {
    "apiKey": "AIzaSyC0GZVwEKNLLcDFSfd3eGBWJbuhZAn4O6A",
    "authDomain": "divergencia-fb3d4.firebaseapp.com",
    "databaseURL": "https://divergencia-fb3d4.firebaseio.com",
    "projectId": "divergencia-fb3d4",
    "storageBucket": "divergencia-fb3d4.appspot.com",
    "messagingSenderId": "1001985982358",
    "appId": "1:1001985982358:web:829168017afc49e10667b7",
}

# Inicializando e autenticando o aplicativo:
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()


# Função para verificar se o usuário e senha inseridas existem no banco de dados Firebase:
def Login():

    st.markdown(
        "<h1 style='text-align: center;'>Gerenciamento de Deem - Login</h1>",
        unsafe_allow_html=True,
    )
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
