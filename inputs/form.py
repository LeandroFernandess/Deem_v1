import streamlit as st
from data.adding_data import AddData
from data.getting_data import get_data
from data.codes import Itens
from data.employees import Employee
from login.login import Login
from export.excel_file import ConvertExcel


def FormDeem():
    # Verificando se o usuário está logado
    if "user_id" not in st.session_state:
        user_id = Login()
        if user_id:
            st.session_state.user_id = user_id
        else:
            st.stop()  # Para a execução se o login não for bem-sucedido
    else:
        user_id = st.session_state.user_id

    st.title("Formulário de Deem's")

    # Obtendo os dados do usuário logado
    user_data = get_data(user_id)

    # Mantendo os valores dos inputs no session state:
    if "name" not in st.session_state:
        st.session_state.name = user_data.get("name", "")
    if "code" not in st.session_state:
        st.session_state.code = user_data.get("code", "")
    if "quantity" not in st.session_state:
        st.session_state.quantity = user_data.get("quantity", "")
    if "rc" not in st.session_state:
        st.session_state.rc = user_data.get("rc", "")
    if "observation" not in st.session_state:
        st.session_state.observation = user_data.get("observation", "")

    # Criando os inputs para o usuário:
    input_name = st.text_input(
        "Nome",
        value=st.session_state.name,
        key="input_name",
        placeholder="Insira o nome do responsável pela notificação da Deem",
    )

    input_code = st.text_input("Código", value=st.session_state.code, key="input_code")

    input_quantity = st.text_input(
        "Quantidade", value=st.session_state.quantity, key="input_quantity"
    )

    input_rc = st.text_input(
        "Relação de Carga", value=st.session_state.rc, key="input_rc"
    )

    input_area = st.selectbox("Área", options=["CLP1", "CLP2"], key="input_area")

    input_observation = st.text_area(
        "Observação",
        key="input_observation",
        value=st.session_state.observation,
        placeholder="Insira informações adicionais ao ocorrido.",
    )

    input_type = st.selectbox(
        "Tipo",
        options=["Maior", "Menor"],
        key="input_type",
    )

    input_files = st.file_uploader(
        "Imagem", accept_multiple_files=True, key="input_file"
    )

    if st.button("Confirmar Deem"):
        if input_code and input_code and input_name:
            AddData(
                input_name,
                input_code,
                input_quantity,
                input_rc,
                input_area,
                input_observation,
                input_type,
                input_files,
                user_id,
            )
            st.success("Divergência inserida com sucesso!")
        else:
            st.error(
                "Por favor, preencha todos os campos obrigatórios. (Nome, Código e Quantidade)"
            )

    Table = get_data()  # Obtendo todos os dados
    st.dataframe(Table)

    if not Table.empty:
        excel_data = ConvertExcel(Table)
        st.download_button(
            label="Extrair para Excel",
            data=excel_data,
            file_name="Deem.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
