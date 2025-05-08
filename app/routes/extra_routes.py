from flask import Blueprint, request, jsonify
from app.db import mongo
from bson import ObjectId

extra_bp = Blueprint('extra_bp', __name__)

@extra_bp.route('/extras', methods=['POST'])
def criar_extra():
    """
    Registra um valor extra vinculado a uma obra.
    Campos obrigatórios: obra_id, valor, descricao, data
    """
    data = request.get_json()

    if not data or not all(k in data for k in ("obra_id", "valor", "descricao", "data")):
        return jsonify({"error": "Campos 'obra_id', 'valor', 'descricao' e 'data' são obrigatórios."}), 400

    try:
        obra_id = ObjectId(data["obra_id"])
    except:
        return jsonify({"error": "obra_id inválido."}), 400

    if not mongo.db.obras.find_one({"_id": obra_id}):
        return jsonify({"error": "Obra não encontrada."}), 404

    novo_extra = {
        "obra_id": obra_id,
        "valor": float(data["valor"]),
        "descricao": data["descricao"],
        "data": data["data"]
    }

    mongo.db.extras.insert_one(novo_extra)

    return jsonify({"message": "Extra registrado com sucesso!"}), 201

@extra_bp.route('/extras', methods=['GET'])
def listar_extras():
    """
    Lista todos os extras com dados da obra associada.
    """
    extras = mongo.db.extras.find()
    resultado = []

    for e in extras:
        obra = mongo.db.obras.find_one({"_id": e["obra_id"]})
        resultado.append({
            "_id": str(e["_id"]),
            "valor": e["valor"],
            "descricao": e["descricao"],
            "data": e["data"],
            "obra": {
                "_id": str(obra["_id"]),
                "nome": obra["nome"]
            } if obra else None
        })

    return jsonify(resultado)


@extra_bp.route('/extras/<extra_id>', methods=['PUT'])
def atualizar_extra(extra_id):
    """
    Atualiza os dados de um valor extra (valor, descrição, data).
    """
    data = request.get_json()

    try:
        extra_oid = ObjectId(extra_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    extra = mongo.db.extras.find_one({"_id": extra_oid})
    if not extra:
        return jsonify({"error": "Extra não encontrado."}), 404

    update_data = {}
    if "valor" in data:
        update_data["valor"] = float(data["valor"])
    if "descricao" in data:
        update_data["descricao"] = data["descricao"]
    if "data" in data:
        update_data["data"] = data["data"]

    if not update_data:
        return jsonify({"error": "Nenhum campo válido para atualização."}), 400

    mongo.db.extras.update_one({"_id": extra_oid}, {"$set": update_data})

    return jsonify({"message": "Extra atualizado com sucesso."})


@extra_bp.route('/extras/<extra_id>', methods=['DELETE'])
def deletar_extra(extra_id):
    """
    Remove um extra do banco.
    """
    try:
        extra_oid = ObjectId(extra_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    resultado = mongo.db.extras.delete_one({"_id": extra_oid})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Extra não encontrado."}), 404

    return jsonify({"message": "Extra deletado com sucesso."})
