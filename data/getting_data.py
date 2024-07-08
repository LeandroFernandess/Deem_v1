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


def GetData(user_id=None):
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


# Função para obter dados do Firestore e editar
def GetDataToEdit(user_id=None):
    db = firestore.client()
    if user_id:
        docs = db.collection("users").where("user_id", "==", user_id).stream()
    else:
        docs = db.collection("users").stream()
    data = [doc.to_dict() for doc in docs]
    return pd.DataFrame(data)


# Função para atualizar dados no Firestore
def UpdateData(document_id, updated_data):
    db = firestore.client()
    doc_ref = db.collection("users").document(document_id)
    doc_ref.update(updated_data)
