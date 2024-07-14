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
            data_dict = doc.to_dict()

            # Se a coluna "Data" existir, assegurar que está no formato ISO8601
            if "Data" in data_dict:
                try:
                    data_dict["Data"] = pd.to_datetime(data_dict["Data"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                except ValueError:
                    data_dict["Data"] = str(data_dict["Data"])

            # Garantir que Imagem seja uma lista de URLs se existir
            if "Imagem" in data_dict and isinstance(data_dict["Imagem"], list):
                data_dict["Imagem"] = data_dict["Imagem"]
            else:
                data_dict["Imagem"] = []

            data.append(data_dict)

        df = pd.DataFrame(data)

        # Garantir que "Data" está como string no DataFrame
        if "Data" in df.columns:
            df["Data"] = df["Data"].astype(str)

        return df


def GetDataToEdit(user_id=None):
    db = firestore.client()
    if user_id:
        docs = db.collection("users").where("user_id", "==", user_id).stream()
    else:
        docs = db.collection("users").stream()
    data = []
    for doc in docs:
        data_dict = doc.to_dict()

        # Garantir que Imagem seja uma lista de URLs se existir
        if "Imagem" in data_dict and isinstance(data_dict["Imagem"], list):
            data_dict["Imagem"] = data_dict["Imagem"]
        else:
            data_dict["Imagem"] = []

        data.append(data_dict)
    return pd.DataFrame(data)


def UpdateData(document_id, updated_data):
    db = firestore.client()
    doc_ref = db.collection("users").document(document_id)
    doc_ref.update(updated_data)
