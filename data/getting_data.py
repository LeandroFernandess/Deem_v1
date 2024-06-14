import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pandas as pd

# Inicializando o serviço do banco de dados Firebase:
try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred)

database = firestore.client()


# Criando a função para pegar as informações do banco de dados Firebase e exibir na tabela da página:
def get_data(user_id=None):
    if user_id:
        user_ref = database.collection("users").document(user_id)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict()
        else:
            return {}
    else:
        users_ref = database.collection("users")
        docs = users_ref.stream()

        data = []
        for doc in docs:
            data.append(doc.to_dict())

        return pd.DataFrame(data)
