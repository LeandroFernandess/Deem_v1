import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime

# Inicializando o serviço do banco de dados Firebase
try:
    firebase_admin.get_app()
except ValueError as e:
    cred = credentials.Certificate("credentials.json")
    firebase_admin.initialize_app(cred, {"storageBucket": "deem-fa6c8.appspot.com"})

database = firestore.client()


# Função para adicionar imagem no Firebase Storage
def AddImage(uploaded_file, user_id):
    bucket = storage.bucket()
    blob = bucket.blob(
        f"{user_id}/{datetime.now().strftime('%Y%m%d%H%M%S')}_{uploaded_file.name}"
    )
    blob.upload_from_string(uploaded_file.getvalue(), content_type=uploaded_file.type)
    return blob.public_url


# Modificando a função `AddData` para aceitar os novos parâmetros
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
    comment,
    type,
    files,
    date,
    user_id,
):

    # Gerando URLs das imagens (não alterado)
    file_urls = [AddImage(file, user_id) for file in files if file is not None]

    # Definindo status fixo
    status = "Pendente de análise"

    # Contar o número atual de documentos na coleção
    collection_ref = database.collection("users")
    documents = collection_ref.stream()
    count = sum(1 for _ in documents)

    # Gerar o próximo num_id
    next_num_id = count + 1

    # Criar referência ao documento e definir os dados
    doc_ref = collection_ref.document()
    doc_ref.set(
        {
            "ID": doc_ref.id,
            "Numero": next_num_id,  # Adicionar o identificador numérico
            "Responsavel": name,
            "Codigo": code,
            "Descricao": description,
            "Quantidade": quantity,
            "Valor Unitario": std,
            "Valor Total": total,
            "RC": rc,
            "Area": area,
            "Observacao": observation,
            "Comentario": comment,  # Adicionando o campo de comentário
            "Tipo": type,
            "Imagem": file_urls,
            "Data": date,
            "Status": status,  # Passando o valor fixo para Status
        }
    )
