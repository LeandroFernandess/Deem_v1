from data.getting_data import GetData, GetDataToEdit, UpdateData
import streamlit as st
from login.login import Login
from information.filters import filters
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

    #  Autenticação adicional para acessar a página de edições
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

    Table = GetData()

    if Table.empty:
        st.warning(
            "Nenhum dado inserido no banco de dados, por favor, preencha o formulário para visualizar os dados"
        )
    else:
        desired_columns = [
            "ID",
            "Numero",
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

            # Ordenar a tabela com base no num_id
            Table = Table.sort_values(by="Numero")

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
                height=400,
                reload_data=True,
            )
            st.write("---")
            # Mapear num_id para índices do DataFrame
            num_id_to_index = {row["Numero"]: index for index, row in Table.iterrows()}

            selected_num_id = st.selectbox(
                "Selecione o Número para editar", options=Table["Numero"]
            )

            selected_row_idx = num_id_to_index[selected_num_id]

            if selected_row_idx is not None:
                selected_row = Table.loc[selected_row_idx].to_dict()
                for column in desired_columns:
                    st.session_state.editable_data[column] = st.text_input(
                        f"Editar {column}",
                        value=selected_row[column],
                        key=f"{selected_row['ID']}-{column}",  # Certifique-se de usar 'ID' aqui
                    )

                if st.button("Salvar Alterações"):
                    updated_data = {
                        f"`{column}`": st.session_state.editable_data[column]
                        for column in desired_columns
                        if column not in ["ID", "Numero"]
                    }  # Excluindo 'ID' e 'num_id' de serem atualizados
                    UpdateData(
                        selected_row["ID"], updated_data
                    )  # Usando 'ID' para identificar o documento
                    st.success("Dados atualizados com sucesso!")
