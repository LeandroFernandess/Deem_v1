from data.getting_data import GetData
import streamlit as st
from login.login import Login
from export.excel_file import ConvertExcel, ConvertCSV
from information.filters import filters
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode, AgGridTheme



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

    # Obter os dados:
    Table = GetData()

    # Verificar se o DataFrame não está vazio e exibir uma mensagem caso contrário:
    if Table.empty:
        st.warning(
            "Nenhum dado inserido no banco de dados, por favor, preencha o formulário para visualizar os dados"
        )
    else:
        # Garantir a coluna "Data" está como string
        if "Data" in Table.columns:
            Table["Data"] = Table["Data"].astype(str)

        # selecionar e ordenar as colunas:
        desired_columns = [
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
            "Comentario",
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
