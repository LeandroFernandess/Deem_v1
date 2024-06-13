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
    st.title("Formulário de Deem")
    code = st.text_input("Código")
    quantity = st.text_input("Quantidade")
    description = st.text_input("Descrição", placeholder="Este campo não é obrigatório")
    rc = st.text_input("Relação de Carga")
    type = st.selectbox(label="Tipo da DEEM", options=["Maior", "Menor"], key="input_tipo")

    if st.button("Confirmar Deem"):
        add_to_firestore(code, quantity, description, rc, type)
        st.success("Divergência inserida com sucesso!")

    df = get_data_from_firestore()
    st.dataframe(df)


if __name__ == "__main__":
    app()
