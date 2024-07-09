import streamlit as st


def Logout():

    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.rerun()
