import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Use a service account
try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()


def add_to_firestore(code, quantity, description, rc, type):
    doc_ref = db.collection("users").document()
    doc_ref.set(
        {
            "code": code,
            "quantity": quantity,
            "description": description,
            "rc": rc,
            "type": type,
        }
    )


def get_data_from_firestore():
    users_ref = db.collection("users")
    docs = users_ref.stream()

    data = []
    for doc in docs:
        data.append(doc.to_dict())

    return pd.DataFrame(data)


def app():
    st.title("Formulário Streamlit Firebase")
    code = st.text_input("Código")
    quantity = st.text_input("Quantidade")
    description = st.text_input("Descrição")
    rc = st.text_input("Relação de Carga")
    type = st.text_input("Tipo")

    if st.button("Enviar"):
        add_to_firestore(code, quantity, description, rc, type)
        st.success("Informações adicionadas ao Firebase")

    df = get_data_from_firestore()
    st.dataframe(df)


if __name__ == "__main__":
    app()
