from data.getting_data import GetData
import streamlit as st
from authentication.login import Login
from export.excel_file import ConvertExcel, ConvertCSV
from information.filters import filters


def Table():

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
        "<h1 style='text-align: center;'>Relatório de divergências</h1>",
        unsafe_allow_html=True,
    )
    st.write("---")

    # Obtendo os dados do usuário logado:
    user_data = GetData(user_id)

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

    if "status" not in st.session_state:
        st.session_state.status = user_data.get("status", "")

    # Obter os dados:
    Table = GetData()

    # Verificar se o DataFrame não está vazio e exibir uma mensagem caso contrário:
    if Table.empty:
        st.warning(
            "Nenhum dado inserido no banco de dados, por favor, preencha o formulário para visualizar os dados"
        )
    else:
        # Selecionar e ordenar as colunas:
        desired_columns = [
            "Responsavel",
            "Codigo",
            "Descricao",
            "Quantidade",
            "Valor Unitario",
            "Valor Total",
            "Tipo",
            "Area",
            "RC",
            "Observacao",
            "Data",
            "Status",
        ]

        # Garantir que as colunas desejadas estão no DataFrame:
        missing_columns = [col for col in desired_columns if col not in Table.columns]
        if missing_columns:
            st.error(
                f"As seguintes colunas estão faltando no DataFrame: {', '.join(missing_columns)}"
            )
        else:
            Table = Table[desired_columns]

            # Aplicar filtros:
            Table = filters(Table)

            # Exibir o DataFrame filtrado:
            st.dataframe(Table)

            # Permitir download se o DataFrame não estiver vazio:
            if not Table.empty:
                excel_data = ConvertExcel(Table)
                st.download_button(
                    label="Extrair para .xlsx",
                    data=excel_data,
                    file_name="Deem.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                )

                csv_data = ConvertCSV(Table)
                st.download_button(
                    label="Extrair para .csv",
                    data=csv_data,
                    file_name="Deem.csv",
                    mime="text/csv",
                )
