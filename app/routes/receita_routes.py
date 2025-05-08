from flask import Blueprint, request, jsonify
from app.db import mongo
from bson import ObjectId

receita_bp = Blueprint('receita_bp', __name__)


@receita_bp.route('/receitas', methods=['POST'])
def criar_receita():
    """
    Registra uma receita (pagamento recebido) associada a uma obra.
    Campos obrigatórios: obra_id, valor, data_recebimento
    """
    data = request.get_json()

    if not data or not all(k in data for k in ("obra_id", "valor", "data_recebimento")):
        return jsonify({"error": "Campos 'obra_id', 'valor' e 'data_recebimento' são obrigatórios."}), 400

    try:
        obra_id = ObjectId(data["obra_id"])
    except Exception:
        return jsonify({"error": "obra_id inválido."}), 400

    if not mongo.db.obras.find_one({"_id": obra_id}):
        return jsonify({"error": "Obra não encontrada."}), 404

    nova_receita = {
        "obra_id": obra_id,
        "valor": float(data["valor"]),
        "data_recebimento": data["data_recebimento"]
    }

    mongo.db.receitas.insert_one(nova_receita)

    return jsonify({"message": "Receita registrada com sucesso!"}), 201


@receita_bp.route('/receitas', methods=['GET'])
def listar_receitas():
    """
    Lista todas as receitas com dados da obra.
    """
    receitas = mongo.db.receitas.find()
    resultado = []

    for r in receitas:
        obra = mongo.db.obras.find_one({"_id": r["obra_id"]})
        resultado.append({
            "_id": str(r["_id"]),
            "valor": r["valor"],
            "data_recebimento": r["data_recebimento"],
            "obra": {
                "_id": str(obra["_id"]),
                "nome": obra["nome"]
            } if obra else None
        })

    return jsonify(resultado)

@receita_bp.route('/receitas/<receita_id>', methods=['PUT'])
def atualizar_receita(receita_id):
    """
    Atualiza o valor ou a data de uma receita.
    """
    data = request.get_json()

    try:
        receita_oid = ObjectId(receita_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    receita = mongo.db.receitas.find_one({"_id": receita_oid})
    if not receita:
        return jsonify({"error": "Receita não encontrada."}), 404

    update_data = {}
    if "valor" in data:
        update_data["valor"] = float(data["valor"])
    if "data_recebimento" in data:
        update_data["data_recebimento"] = data["data_recebimento"]

    if not update_data:
        return jsonify({"error": "Nenhum campo válido para atualização."}), 400

    mongo.db.receitas.update_one({"_id": receita_oid}, {"$set": update_data})

    return jsonify({"message": "Receita atualizada com sucesso."})


@receita_bp.route('/receitas/<receita_id>', methods=['DELETE'])
def deletar_receita(receita_id):
    """
    Remove uma receita do banco de dados.
    """
    try:
        receita_oid = ObjectId(receita_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    resultado = mongo.db.receitas.delete_one({"_id": receita_oid})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Receita não encontrada."}), 404

    return jsonify({"message": "Receita deletada com sucesso."})
