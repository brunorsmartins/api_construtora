from flask import Blueprint, request, jsonify
from app.db import mongo
from bson import ObjectId

orcamento_bp = Blueprint('orcamento_bp', __name__)

@orcamento_bp.route ('/orcamentos', methods=['POST'])
def criar_orcamento():
    # Cria orçamento para uma obra existente
    # Campos obrigatórios: obra_id, valor, data_orcamento

    data = request.get_json()

    if not data or not all(k in data for k in ("obra_id", "valor", "data_orcamento")):
        return jsonify({"error" : "Campos 'obra_id, 'valor', 'data_orcamento' são obrigatórios"}), 400
    
    try:
        obra_id = ObjectId(data["obra_id"])
    except Exception:
        return jsonify({"error":"Obra não encontrada"}), 400
    
    # Verifica se a obra existe
    if not mongo.db.obras.find_one({"_id": obra_id}):
        return jsonify({"error": "Obra não encontrada."}), 404

    novo_orcamento = {
        "obra_id": obra_id,
        "valor": float(data["valor"]),
        "data_orcamento": data["data_orcamento"]
    }

    mongo.db.orcamentos.insert_one(novo_orcamento)

    return jsonify({"message": "Orçamento criado com sucesso!"}), 201


@orcamento_bp.route('/orcamentos', methods=['GET'])
def listar_orcamentos():
    """
    Lista todos os orçamentos com informações da obra.
    """
    orcamentos = mongo.db.orcamentos.find()
    resultado = []

    for orc in orcamentos:
        obra = mongo.db.obras.find_one({"_id": orc["obra_id"]})
        resultado.append({
            "_id": str(orc["_id"]),
            "valor": orc["valor"],
            "data_orcamento": orc["data_orcamento"],
            "obra": {
                "_id": str(obra["_id"]),
                "nome": obra["nome"]
            } if obra else None
        })

    return jsonify(resultado)


@orcamento_bp.route('/orcamentos/<orcamento_id>', methods=['PUT'])
def atualizar_orcamento(orcamento_id):
    """
    Atualiza o valor ou data de um orçamento.
    """
    data = request.get_json()

    try:
        orcamento_oid = ObjectId(orcamento_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    orcamento = mongo.db.orcamentos.find_one({"_id": orcamento_oid})
    if not orcamento:
        return jsonify({"error": "Orçamento não encontrado."}), 404

    update_data = {}
    if "valor" in data:
        update_data["valor"] = float(data["valor"])
    if "data_orcamento" in data:
        update_data["data_orcamento"] = data["data_orcamento"]

    if not update_data:
        return jsonify({"error": "Nenhum campo válido para atualização."}), 400

    mongo.db.orcamentos.update_one({"_id": orcamento_oid}, {"$set": update_data})

    return jsonify({"message": "Orçamento atualizado com sucesso."})

@orcamento_bp.route('/orcamentos/<orcamento_id>', methods=['DELETE'])
def deletar_orcamento(orcamento_id):
    """
    Remove um orçamento do banco.
    """
    try:
        orcamento_oid = ObjectId(orcamento_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    resultado = mongo.db.orcamentos.delete_one({"_id": orcamento_oid})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Orçamento não encontrado."}), 404

    return jsonify({"message": "Orçamento deletado com sucesso."})

