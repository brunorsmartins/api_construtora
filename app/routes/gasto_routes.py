from flask import Blueprint, request, jsonify
from app.db import mongo
from bson import ObjectId

gasto_bp = Blueprint('gasto_bp', __name__)

RESPONSAVEIS_VALIDOS = [
    "Marcon Credito", "Marcon PIX",
    "Marcio PIX", "Marcio Credito",
    "Celso PIX", "Celso Credito",
    "Bruno PIX"
]

@gasto_bp.route('/gastos', methods=['POST'])
def criar_gasto():
    """
    Registra um gasto, que pode ser geral ou vinculado a uma obra.
    Campos obrigatórios: valor, descricao, data, responsavel
    obra_id é opcional.
    """
    data = request.get_json()

    campos_obrigatorios = ("valor", "descricao", "data", "responsavel")
    if not data or not all(k in data for k in campos_obrigatorios):
        return jsonify({"error": "Campos 'valor', 'descricao', 'data' e 'responsavel' são obrigatórios."}), 400

    if data["responsavel"] not in RESPONSAVEIS_VALIDOS:
        return jsonify({"error": f"Responsável inválido. Use um dos valores permitidos: {RESPONSAVEIS_VALIDOS}"}), 400

    gasto = {
        "valor": float(data["valor"]),
        "descricao": data["descricao"],
        "data": data["data"],
        "responsavel": data["responsavel"]
    }

    if "obra_id" in data and data["obra_id"]:
        try:
            obra_id = ObjectId(data["obra_id"])
            if not mongo.db.obras.find_one({"_id": obra_id}):
                return jsonify({"error": "Obra não encontrada."}), 404
            gasto["obra_id"] = obra_id
        except:
            return jsonify({"error": "obra_id inválido."}), 400

    mongo.db.gastos.insert_one(gasto)
    return jsonify({"message": "Gasto registrado com sucesso!"}), 201

@gasto_bp.route('/gastos', methods=['GET'])
def listar_gastos():
    """
    Lista todos os gastos, com nome da obra se houver vínculo.
    """
    gastos = mongo.db.gastos.find()
    resultado = []

    for g in gastos:
        obra_info = None
        if "obra_id" in g:
            obra = mongo.db.obras.find_one({"_id": g["obra_id"]})
            if obra:
                obra_info = {"_id": str(obra["_id"]), "nome": obra["nome"]}

        resultado.append({
            "_id": str(g["_id"]),
            "valor": g["valor"],
            "descricao": g["descricao"],
            "data": g["data"],
            "responsavel": g["responsavel"],
            "obra": obra_info
        })

    return jsonify(resultado)

@gasto_bp.route('/gastos/<gasto_id>', methods=['PUT'])
def atualizar_gasto(gasto_id):
    """
    Atualiza dados de um gasto (valor, descrição, data, responsável, obra).
    """
    from app.routes.gasto_routes import RESPONSAVEIS_VALIDOS
    data = request.get_json()

    try:
        gasto_oid = ObjectId(gasto_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    gasto = mongo.db.gastos.find_one({"_id": gasto_oid})
    if not gasto:
        return jsonify({"error": "Gasto não encontrado."}), 404

    update_data = {}

    if "valor" in data:
        update_data["valor"] = float(data["valor"])
    if "descricao" in data:
        update_data["descricao"] = data["descricao"]
    if "data" in data:
        update_data["data"] = data["data"]
    if "responsavel" in data:
        if data["responsavel"] not in RESPONSAVEIS_VALIDOS:
            return jsonify({"error": f"Responsável inválido. Use um dos valores: {RESPONSAVEIS_VALIDOS}"}), 400
        update_data["responsavel"] = data["responsavel"]
    if "obra_id" in data and data["obra_id"]:
        try:
            obra_oid = ObjectId(data["obra_id"])
            if not mongo.db.obras.find_one({"_id": obra_oid}):
                return jsonify({"error": "Obra não encontrada."}), 404
            update_data["obra_id"] = obra_oid
        except:
            return jsonify({"error": "obra_id inválido."}), 400

    if not update_data:
        return jsonify({"error": "Nenhum campo válido para atualização."}), 400

    mongo.db.gastos.update_one({"_id": gasto_oid}, {"$set": update_data})

    return jsonify({"message": "Gasto atualizado com sucesso."})


@gasto_bp.route('/gastos/<gasto_id>', methods=['DELETE'])
def deletar_gasto(gasto_id):
    """
    Remove um gasto do banco.
    """
    try:
        gasto_oid = ObjectId(gasto_id)
    except:
        return jsonify({"error": "ID inválido."}), 400

    resultado = mongo.db.gastos.delete_one({"_id": gasto_oid})
    if resultado.deleted_count == 0:
        return jsonify({"error": "Gasto não encontrado."}), 404

    return jsonify({"message": "Gasto deletado com sucesso."})
