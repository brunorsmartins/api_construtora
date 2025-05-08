from flask import Blueprint, request, jsonify
from app.db import mongo
from bson import ObjectId

obra_bp = Blueprint('obra_bp', __name__)

@obra_bp.route('/obras', methods=['GET'])
def listar_obras():
    """
    Lista todas as obras cadastradas com os dados básicos do cliente.
    """
    obras = mongo.db.obras.find()
    resultado = []

    for obra in obras:
        cliente = mongo.db.clientes.find_one({"_id": obra["cliente_id"]})
        resultado.append({
            "_id": str(obra["_id"]),
            "nome": obra["nome"],
            "data_inicio": obra["data_inicio"],
            "status": obra["status"],
            "cliente": {
                "_id": str(cliente["_id"]),
                "nome": cliente["nome"]
            } if cliente else None
        })

    return jsonify(resultado)


@obra_bp.route('/obras', methods=['POST'])
def criar_obra():
    from bson import ObjectId  # ← garante que esteja dentro do escopo, se necessário
    data = request.get_json()

    # Verifica se os campos obrigatórios estão presentes
    if not data or not all(k in data for k in ("nome", "data_inicio", "cliente_id")):
        return jsonify({"error": "Campos 'nome', 'data_inicio' e 'cliente_id' são obrigatórios."}), 400

    try:
        cliente_id = ObjectId(data["cliente_id"])
    except Exception:
        return jsonify({"error": "cliente_id inválido (não é um ObjectId válido)."}), 400

    # Verifica se o cliente existe
    cliente = mongo.db.clientes.find_one({"_id": cliente_id})
    if not cliente:
        return jsonify({"error": "Cliente não encontrado."}), 404

    # Monta o documento da obra
    nova_obra = {
        "nome": data["nome"],
        "data_inicio": data["data_inicio"],
        "status": data.get("status", "ANDAMENTO"),
        "cliente_id": cliente_id
    }

    mongo.db.obras.insert_one(nova_obra)

    return jsonify({"message": "Obra criada com sucesso!"}), 201


@obra_bp.route('/obras/<obra_id>/saldo', methods=['GET'])
def saldo_obra(obra_id):
    """
    Retorna o saldo financeiro da obra:
    saldo = receitas + extras - gastos
    """
    try:
        obra_oid = ObjectId(obra_id)
    except:
        return jsonify({"error": "ID da obra inválido."}), 400

    obra = mongo.db.obras.find_one({"_id": obra_oid})
    if not obra:
        return jsonify({"error": "Obra não encontrada."}), 404

    # Somar receitas
    receitas = mongo.db.receitas.aggregate([
        {"$match": {"obra_id": obra_oid}},
        {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
    ])
    total_receitas = next(receitas, {}).get("total", 0)

    # Somar extras
    extras = mongo.db.extras.aggregate([
        {"$match": {"obra_id": obra_oid}},
        {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
    ])
    total_extras = next(extras, {}).get("total", 0)

    # Somar gastos
    gastos = mongo.db.gastos.aggregate([
        {"$match": {"obra_id": obra_oid}},
        {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
    ])
    total_gastos = next(gastos, {}).get("total", 0)

    # Somar orçamentos
    orcs = mongo.db.orcamentos.aggregate([
        {"$match": {"obra_id": obra_oid}},
        {"$group": {"_id": None, "total": {"$sum": "$valor"}}}
    ])
    total_orcado = next(orcs, {}).get("total", 0)

    saldo = total_receitas + total_extras - total_gastos

    return jsonify({
        "obra_id": obra_id,
        "nome_obra": obra["nome"],
        "orcamento_total": total_orcado,
        "total_recebido": total_receitas,
        "total_extras": total_extras,
        "total_gastos": total_gastos,
        "saldo_final": saldo
    })

@obra_bp.route('/obras/<obra_id>', methods=['PUT'])
def atualizar_obra(obra_id):
    """
    Atualiza os dados de uma obra: nome, data_inicio ou status.
    """
    data = request.get_json()

    try:
        obra_oid = ObjectId(obra_id)
    except:
        return jsonify({"error": "ID da obra inválido."}), 400

    obra = mongo.db.obras.find_one({"_id": obra_oid})
    if not obra:
        return jsonify({"error": "Obra não encontrada."}), 404

    update_data = {}
    for campo in ("nome", "data_inicio", "status"):
        if campo in data:
            update_data[campo] = data[campo]

    if not update_data:
        return jsonify({"error": "Nenhum campo válido para atualização."}), 400

    mongo.db.obras.update_one({"_id": obra_oid}, {"$set": update_data})

    return jsonify({"message": "Obra atualizada com sucesso."})

@obra_bp.route('/obras/<obra_id>', methods=['DELETE'])
def deletar_obra(obra_id):
    """
    Remove uma obra do banco de dados.
    """
    try:
        obra_oid = ObjectId(obra_id)
    except:
        return jsonify({"error": "ID da obra inválido."}), 400

    resultado = mongo.db.obras.delete_one({"_id": obra_oid})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Obra não encontrada."}), 404

    return jsonify({"message": "Obra deletada com sucesso."})
