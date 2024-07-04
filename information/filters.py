import streamlit as st
import pandas as pd


def filters(Table):

    # Criar duas colunas para os filtros:
    col1, col2, col3 = st.columns(3)

    # Filtrar os dados por responsável:
    responsible = Table["Responsável"].unique()
    selected_responsible = col1.multiselect(
        "Filtrar por Responsável",
        responsible,
        placeholder="Escolha um responsável",
    )
    if selected_responsible:
        Table = Table[Table["Responsável"].isin(selected_responsible)]

    # Filtrar os dados por código:
    code_filter = col1.text_input(
        "Filtrar por código", value="", placeholder="Digite um código"
    )
    if code_filter:
        Table = Table[Table["Código"].str.contains(code_filter, case=False, na=False)]

    # Filtrar os dados por descrição:
    description_filter = col1.text_input(
        "Filtrar por descrição", value="", placeholder="Digite uma descrição"
    )
    if description_filter:
        Table = Table[
            Table["Descrição"].str.contains(description_filter, case=False, na=False)
        ]

    # Filtrar os dados por tipo:
    type_filter = col2.text_input(
        "Filtrar por tipo", value="", placeholder="Digite o tipo da Deem"
    )
    if type_filter:
        Table = Table[Table["Tipo"].str.contains(type_filter, case=False, na=False)]

    # Filtrar os dados por RC:
    rc_filter = col2.text_input(
        "Filtrar por Relação de Carga",
        value="",
        placeholder="Digite a Relação de Carga",
    )
    if rc_filter:
        Table = Table[Table["RC"].str.contains(rc_filter, case=False, na=False)]

    # Converter a coluna de data para datetime:
    Table = Table.copy()  # Adicionado para evitar o aviso de SettingWithCopyWarning
    Table.loc[:, "Data"] = pd.to_datetime(Table["Data"], errors="coerce")

    # Filtrar os dados por data:
    start_date = col3.date_input("Data de início", value=pd.to_datetime("2024-01-01"))
    end_date = col3.date_input("Data de término", value=pd.to_datetime("today"))

    if start_date and end_date:
        Table = Table[
            (Table["Data"] >= pd.to_datetime(start_date))
            & (Table["Data"] <= pd.to_datetime(end_date))
        ]

    return Table
