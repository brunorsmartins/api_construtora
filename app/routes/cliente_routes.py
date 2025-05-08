from flask import Blueprint, request, jsonify
from app.db import mongo
from bson import ObjectId

# Criamos o blueprint da rota cliente
cliente_bp = Blueprint('cliente_bp', __name__)

@cliente_bp.route('/clientes', methods=['GET'])
def listar_clientes():
    """
    Lista todos os clientes cadastrados na coleção 'clientes'.
    """
    clientes = mongo.db.clientes.find()

    # Transformamos os documentos em um formato JSON serializável
    resultado = []
    for cliente in clientes:
        resultado.append({
            "_id": str(cliente["_id"]),
            "nome": cliente["nome"],
            "documento": cliente["documento"]
        })

    return jsonify(resultado)

@cliente_bp.route('/clientes', methods=['POST'])
def adicionar_cliente():
    """
    Adiciona um cliente com nome e documento (CPF/CNPJ).
    """
    data = request.get_json()

    if not data or not all(k in data for k in ("nome", "documento")):
        return jsonify({"error": "Campos 'nome' e 'documento' são obrigatórios."}), 400

    mongo.db.clientes.insert_one({
        "nome": data["nome"],
        "documento": data["documento"]
    })

    return jsonify({"message": "Cliente adicionado com sucesso!"}), 201

@cliente_bp.route('/clientes/<cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    """
    Atualiza o nome ou documento de um cliente existente.
    """
    data = request.get_json()

    try:
        cliente_oid = ObjectId(cliente_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    cliente = mongo.db.clientes.find_one({"_id": cliente_oid})
    if not cliente:
        return jsonify({"error": "Cliente não encontrado."}), 404

    update_data = {}
    if "nome" in data:
        update_data["nome"] = data["nome"]
    if "documento" in data:
        update_data["documento"] = data["documento"]

    if not update_data:
        return jsonify({"error": "Nenhum campo válido para atualização."}), 400

    mongo.db.clientes.update_one({"_id": cliente_oid}, {"$set": update_data})

    return jsonify({"message": "Cliente atualizado com sucesso."})

@cliente_bp.route('/clientes/<cliente_id>', methods=['DELETE'])
def deletar_cliente(cliente_id):
    """
    Remove um cliente do banco de dados.
    """
    try:
        cliente_oid = ObjectId(cliente_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    resultado = mongo.db.clientes.delete_one({"_id": cliente_oid})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Cliente não encontrado."}), 404

    return jsonify({"message": "Cliente deletado com sucesso."})