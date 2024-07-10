from Data.Getting_data import GetData, GetDataToEdit, UpdateData
import streamlit as st
from Authentication.login import Login
from Information.Filters import filters
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, AgGridTheme

# Senha para acesso à página de edições
password = "123456"


def Edits():

    if "editable_data" not in st.session_state:
        st.session_state.editable_data = {}

    if "user_id" not in st.session_state:
        user_id = Login()
        if user_id:
            st.session_state.user_id = user_id
        else:
            st.stop()
    else:
        user_id = st.session_state.user_id

    # Autenticação adicional para acessar a página de edições
    if "edit_page_access" not in st.session_state:
        st.session_state.edit_page_access = False

    if not st.session_state.edit_page_access:
        edit_page_password = st.text_input(
            "Insira a senha para acessar o menu de edições", type="password"
        )

        if st.button("Acessar página de edições"):
            if edit_page_password == password:
                st.session_state.edit_page_access = True
                st.rerun()
            else:
                st.error("Você não possui acesso a essa transação.")
                st.stop()

    if not st.session_state.edit_page_access:
        st.stop()

    st.markdown(
        "<h1 style='text-align: center;'>Editar divergências</h1>",
        unsafe_allow_html=True,
    )
    st.write("---")

    user_data = GetData(user_id)

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

    Table = GetDataToEdit()

    if Table.empty:
        st.warning(
            "Nenhum dado inserido no banco de dados, por favor, preencha o formulário para visualizar os dados"
        )
    else:
        desired_columns = [
            "ID",
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

        missing_columns = [col for col in desired_columns if col not in Table.columns]
        if missing_columns:
            st.error(
                f"As seguintes colunas estão faltando no DataFrame: {', '.join(missing_columns)}"
            )
        else:
            Table = Table[desired_columns]

            # Aplicar filtros:
            Table = filters(Table)

            # Configurar opções da tabela:
            gb = GridOptionsBuilder.from_dataframe(Table)
            gridOptions = gb.build()

            st.write("---")

            # Exibir a tabela interativa:
            AgGrid(
                Table,
                gridOptions=gridOptions,
                columns_auto_size_mode=ColumnsAutoSizeMode.FIT_ALL_COLUMNS_TO_VIEW,
                theme=AgGridTheme.STREAMLIT,
                update_mode="MODEL_CHANGED",
                fit_columns_on_grid_load=False,
                enable_enterprise_modules=False,
                height=200,
                reload_data=True,
            )
            st.write("---")
            selected_row_idx = st.selectbox(
                "Selecione a linha para editar", Table.index
            )

            if selected_row_idx is not None:
                selected_row = Table.loc[selected_row_idx].to_dict()
                for column in desired_columns:
                    st.session_state.editable_data[column] = st.text_input(
                        f"Editar {column}",
                        value=selected_row[column],
                        key=f"{selected_row['ID']}-{column}",
                    )

                if st.button("Salvar Alterações"):
                    updated_data = {
                        f"`{column}`": st.session_state.editable_data[column]
                        for column in desired_columns
                        if column != "ID"
                    }
                    UpdateData(selected_row["ID"], updated_data)
                    st.success("Dados atualizados com sucesso!")
