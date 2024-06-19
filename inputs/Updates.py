import streamlit as st
from data.codes import Itens


def UpdateDescription():
    code = st.session_state.input_code
    itens_dict = Itens()
    if code in itens_dict:
        st.session_state.input_description = itens_dict[code]["Texto breve material"]
        price = itens_dict[code]["Preço"]
        st.session_state.input_std = (
            f"R$ {price:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
        st.session_state.raw_price = price  # Armazena o preço bruto para cálculos
    else:
        st.session_state.input_description = ""
        st.session_state.input_std = ""
        st.session_state.raw_price = 0
        st.error(
            "Código inserido não está cadastrado no banco de dados, verifique a informação inserida e se o erro persistir procure seu gestor."
        )
        st.session_state.input_code = ""


def CalculateTotal():
    try:
        quantity = float(st.session_state.input_quantity)
        std = float(st.session_state.raw_price)  # Usa o preço bruto para cálculos
        total = quantity * std
        st.session_state.input_total = (
            f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        )
    except ValueError:
        st.session_state.input_total = ""
