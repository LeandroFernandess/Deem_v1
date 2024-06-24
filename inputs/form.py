import streamlit as st
from data.adding_data import AddData
from data.getting_data import get_data
from login.login import Login
from inputs.Updates import UpdateDescription, CalculateTotal


def FormDeem():

    # Verificando se o usuário está logado:

    if "user_id" not in st.session_state:
        user_id = Login()
        if user_id:
            st.session_state.user_id = user_id
        else:
            st.stop()
    else:
        user_id = st.session_state.user_id

    # Criando o título do formulário:

    st.markdown(
        "<h1 style='text-align: center;'>Formulário de divergências</h1>",
        unsafe_allow_html=True,
    )
    st.write("---")

    # Obtendo os dados do usuário logado:

    user_data = get_data(user_id)

    # Mantendo os valores dos inputs no session state:

    if "name" not in st.session_state:
        st.session_state.name = user_data.get("name", "")

    if "code" not in st.session_state:
        st.session_state.code = user_data.get("code", "")

    if "quantity" not in st.session_state:
        st.session_state.quantity = user_data.get("quantity", "")

    if "std" not in st.session_state:
        price = user_data.get("std", 0)
        st.session_state.std = (
            f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )

    if "input_total" not in st.session_state:
        st.session_state.input_total = ""

    if "rc" not in st.session_state:
        st.session_state.rc = user_data.get("rc", "")

    if "observation" not in st.session_state:
        st.session_state.observation = user_data.get("observation", "")

    if "input_description" not in st.session_state:
        st.session_state.input_description = user_data.get("description", "")

    # Criando os inputs para o usuário:

    input_name = st.text_input(
        "Nome",
        value=st.session_state.name,
        key="input_name",
        placeholder="Insira o nome do responsável pela notificação da Deem",
    )

    input_code = st.text_input(
        "Código",
        value=st.session_state.code,
        key="input_code",
        on_change=UpdateDescription,
    )

    input_description = st.text_input(
        "Descrição do material",
        value="",
        key="input_description",
        disabled=True,
    )

    input_quantity = st.text_input(
        "Quantidade",
        value=st.session_state.quantity,
        key="input_quantity",
        on_change=CalculateTotal,
    )

    input_std = st.text_input(
        "Valor Unitário",
        value="",
        key="input_std",
        disabled=True,
    )

    input_total = st.text_input(
        "Valor Total",
        value="",
        key="input_total",
        disabled=True,
    )

    input_rc = st.text_input(
        "Relação de Carga", value=st.session_state.rc, key="input_rc"
    )

    input_type = st.selectbox(
        "Tipo da Deem",
        options=["Maior", "Menor"],
        key="input_type",
    )

    input_area = st.selectbox(
        "Área de recebimento", options=["CLP1", "CLP2"], key="input_area"
    )

    input_observation = st.text_area(
        "Observação",
        key="input_observation",
        value=st.session_state.observation,
        placeholder="Insira informações adicionais ao ocorrido",
    )

    input_files = st.file_uploader(
        "Imagem", accept_multiple_files=True, key="input_file"
    )

    input_date = st.date_input("Data do ocorrido", format="DD/MM/YYYY")

    if st.button("Confirmar Deem"):

        # Inserindo as informações dos inputs no banco de dados:

        if input_code and input_name and input_quantity:
            input_date = input_date.strftime("%Y-%m-%d")
            AddData(
                input_name,
                input_code,
                input_description,
                input_quantity,
                input_std,
                input_total,
                input_rc,
                input_area,
                input_observation,
                input_type,
                input_files,
                input_date,
                user_id,
            )
            st.success(
                "Divergência inserida com sucesso! Você pode verificar a informação na guia **Visão Geral**"
            )
        else:
            st.error(
                "Por favor, preencha todos os campos obrigatórios. (Nome, Código e Quantidade)"
            )
