import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime

# Inicializando o serviço do banco de dados Firebase:

try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "deem-fa6c8.appspot.com"})

database = firestore.client()


def AddImage(uploaded_file, user_id):
    bucket = storage.bucket()
    blob = bucket.blob(
        f"{user_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
    )
    blob.upload_from_string(uploaded_file.getvalue(), content_type=uploaded_file.type)
    return blob.public_url


def AddData(
    name,
    code,
    description,
    quantity,
    std,
    total,
    rc,
    area,
    observation,
    type,
    files,
    date,
    user_id,
):

    # Gerando URLs das imagens (não alterado)
    file_urls = [AddImage(file, user_id) for file in files]

    # Definindo status fixo
    status = "Pendente de análise"

    # Criando referência ao documento e definindo os dados
    doc_ref = database.collection("users").document()
    doc_ref.set(
        {
            "ID": doc_ref.id,
            "Responsavel": name,
            "Codigo": code,
            "Descricao": description,
            "Quantidade": quantity,
            "Valor Unitario": std,
            "Valor Total": total,
            "RC": rc,
            "Area": area,
            "Observacao": observation,
            "Tipo": type,
            "Imagem": file_urls,
            "Data": date,
            "Status": status,  # Passando o valor fixo para Status
        }
    )
