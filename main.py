import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from data.adding_data import add_data
from data.getting_data import get_data
from login.login import login_user
from export.excel_file import convert_df_to_excel

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

        # Verificando se o usuário está logado
        if "user_id" not in st.session_state:
            user_id = login_user()
            if user_id:
                st.session_state.user_id = user_id
            else:
                st.stop()  # Para a execução se o login não for bem-sucedido
        else:
            user_id = st.session_state.user_id

        st.title("Formulário de Deem's")

        # Obtendo os dados do usuário logado
        user_data = get_data(user_id)

        # Mantendo os valores dos inputs no session state
        if "name" not in st.session_state:
            st.session_state.name = user_data.get("name", "")
        if "code" not in st.session_state:
            st.session_state.code = user_data.get("code", "")
        if "quantity" not in st.session_state:
            st.session_state.quantity = user_data.get("quantity", "")
        if "rc" not in st.session_state:
            st.session_state.rc = user_data.get("rc", "")
        if "type" not in st.session_state:
            st.session_state.type = user_data.get("type", "")

        name = st.text_input(
            "Nome",
            value=st.session_state.name,
            key="name",
            placeholder="Insira o nome do responsável pela notificação da Deem",
        )
        code = st.text_input("Código", value=st.session_state.code, key="code")
        quantity = st.text_input(
            "Quantidade", value=st.session_state.quantity, key="quantity"
        )
        rc = st.text_input("Relação de Carga", value=st.session_state.rc, key="rc")
        type = st.text_input("Tipo", value=st.session_state.type, key="type")

        if st.button("Confirmar Deem"):
            if (
                code and quantity and type
            ):  # Verificando se todos os campos foram preenchidos
                add_data(name, code, quantity, rc, type)
                st.success("Divergência inserida com sucesso!")
            else:
                st.error("Por favor, preencha todos os campos.")

        # Exibindo o DataFrame
        df = get_data()  # Obtendo todos os dados
        st.dataframe(df)

        # Verificando se o DataFrame não está vazio antes de exibir o botão
        if not df.empty:
            excel_data = convert_df_to_excel(df)
            st.download_button(
                label="Extrair para Excel",
                data=excel_data,
                file_name="Deem.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    if option == "Recarregar 🔃":
        pass


if __name__ == "__main__":
    app()
