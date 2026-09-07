from pymongo import MongoClient
from pymongo.errors import PyMongoError


# String de conexão com o cluster do MongoDB Atlas
URI = (
    f"mongodb+srv://borbaf_db_user:{borbaF123}"
    "@clusterfb.xwsr3hd.mongodb.net/"
    "?retryWrites=true&w=majority"
)

# Banco de dados e collection alvo
NOME_BANCO = "teste_fb"
NOME_COLLECTION = "aula"


def main():
    # Documentos de exemplo com dados logísticos
    documentos = [
        {
            "origem": "São Paulo - SP",
            "destino": "Rio de Janeiro - RJ",
            "produto": "Eletrônicos",
            "peso": 12.5,
            "status": "em trânsito",
        },
        {
            "origem": "Belo Horizonte - MG",
            "destino": "Curitiba - PR",
            "produto": "Móveis",
            "peso": 45.0,
            "status": "entregue",
        },
        {
            "origem": "Porto Alegre - RS",
            "destino": "Florianópolis - SC",
            "produto": "Alimentos perecíveis",
            "peso": 8.3,
            "status": "aguardando coleta",
        },
        {
            "origem": "Salvador - BA",
            "destino": "Recife - PE",
            "produto": "Material de construção",
            "peso": 120.0,
            "status": "em trânsito",
        },
        {
            "origem": "Fortaleza - CE",
            "destino": "Manaus - AM",
            "produto": "Eletrodomésticos",
            "peso": 33.7,
            "status": "entregue",
        },
    ]

    try:
        # Conectando ao MongoDB Atlas
        cliente = MongoClient(URI)
        banco = cliente[NOME_BANCO]
        collection = banco[NOME_COLLECTION]

        print(f"Inserindo documentos na collection '{NOME_COLLECTION}'...")
        resultado = collection.insert_many(documentos)

        print(f"Quantidade de documentos inseridos: {len(resultado.inserted_ids)}")
        print("IDs inseridos:")
        for doc_id in resultado.inserted_ids:
            print(f"  - {doc_id}")

        # Consultando para confirmar a inserção
        print("\nDocumentos encontrados na collection:")
        for documento in collection.find():
            print(documento)

    except PyMongoError as erro:
        print(f"Erro ao interagir com o MongoDB: {erro}")
    finally:
        cliente.close()


if __name__ == "__main__":
    main()