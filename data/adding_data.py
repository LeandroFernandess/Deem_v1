# Importando as bibliotecas necessárias:


import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


# Inicializando o serviço do banco de dados Firebase:


try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)

database = firestore.client()


# Criando a função para adicionar as informações do formulário no banco de dados Firebase:


def add_data(code, quantity, description, rc, type):
    doc_ref = database.collection("users").document()
    doc_ref.set(
        {
            "code": code,
            "quantity": quantity,
            "description": description,
            "rc": rc,
            "type": type,
        }
    )
