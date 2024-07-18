""" Importando a biblioteca necessária """

import streamlit as st

"""

- Objetivo da Função: A função `Logout` é usada para desconectar um usuário.
- Funcionalidades: 
  - Marca o status do usuário (`logged_in`) como `False`.
  - Remove a identificação do usuário (`user_id`) definindo-a como `None`.
  - Reinicia a aplicação para aplicar imediatamente essas mudanças.

"""


def Logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.rerun()
