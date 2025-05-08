from app import create_app
from app.db import mongo

# Criar a aplicação Flask e inicializar o Mongo
app = create_app()

# Executa os comandos dentro do contexto do app
with app.app_context():
    print("Conectado ao MongoDB!")

    # Inserir um cliente de teste
    resultado = mongo.db.clientes.insert_one({
        "nome": "Cliente Exemplo",
        "documento": "12345678900"
    })
    print(f"Cliente inserido com _id: {resultado.inserted_id}")

    # Listar todos os clientes da coleção
    print("Clientes no banco:")
    for cliente in mongo.db.clientes.find():
        print(f"- {cliente['nome']} ({cliente['documento']})")
