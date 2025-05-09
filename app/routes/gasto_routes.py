from flask_restx import Namespace, Resource, fields
from flask import request
from app.db import mongo
from bson import ObjectId

ns = Namespace('gastos', description='Operações com gastos (comuns ou por obra)')

RESPONSAVEIS_VALIDOS = [
    "Marcon Credito", "Marcon PIX", "Marcio PIX",
    "Marcio Credito", "Celso PIX", "Celso Credito", "Bruno PIX"
]

gasto_model = ns.model('Gasto', {
    'valor': fields.Float(required=True, description='Valor gasto'),
    'descricao': fields.String(required=True, description='Descrição do gasto'),
    'data': fields.String(required=True, description='Data do gasto'),
    'responsavel': fields.String(required=True, description='Quem pagou o gasto'),
    'obra_id': fields.String(required=False, description='ID da obra (opcional)')
})

@ns.route('/')
class GastoList(Resource):
    @ns.doc('listar_gastos')
    def get(self):
        gastos = mongo.db.gastos.find()
        resultado = []
        for g in gastos:
            resultado.append({
                "_id": str(g["_id"]),
                "valor": g["valor"],
                "descricao": g["descricao"],
                "data": g["data"],
                "responsavel": g["responsavel"],
                "obra_id": str(g["obra_id"]) if "obra_id" in g else None
            })
        return resultado

    @ns.doc('criar_gasto')
    @ns.expect(gasto_model)
    def post(self):
        data = request.get_json()

        if not data or not all(k in data for k in ("valor", "descricao", "data", "responsavel")):
            return {"error": "Campos obrigatórios faltando"}, 400

        if data["responsavel"] not in RESPONSAVEIS_VALIDOS:
            return {"error": f"Responsável inválido. Use um dos valores: {RESPONSAVEIS_VALIDOS}"}, 400

        novo_gasto = {
            "valor": float(data["valor"]),
            "descricao": data["descricao"],
            "data": data["data"],
            "responsavel": data["responsavel"]
        }

        if "obra_id" in data and data["obra_id"]:
            try:
                obra_oid = ObjectId(data["obra_id"])
                if not mongo.db.obras.find_one({"_id": obra_oid}):
                    return {"error": "Obra não encontrada"}, 404
                novo_gasto["obra_id"] = obra_oid
            except:
                return {"error": "obra_id inválido"}, 400

        mongo.db.gastos.insert_one(novo_gasto)
        return {"message": "Gasto registrado com sucesso"}, 201


@ns.route('/<string:gasto_id>')
@ns.param('gasto_id', 'ID do gasto')
class Gasto(Resource):
    def put(self, gasto_id):
        data = request.get_json()

        try:
            oid = ObjectId(gasto_id)
        except:
            return {"error": "ID inválido"}, 400

        if not mongo.db.gastos.find_one({"_id": oid}):
            return {"error": "Gasto não encontrado"}, 404

        update_data = {}
        if "valor" in data:
            update_data["valor"] = float(data["valor"])
        if "descricao" in data:
            update_data["descricao"] = data["descricao"]
        if "data" in data:
            update_data["data"] = data["data"]
        if "responsavel" in data:
            if data["responsavel"] not in RESPONSAVEIS_VALIDOS:
                return {"error": f"Responsável inválido. Use um dos valores: {RESPONSAVEIS_VALIDOS}"}, 400
            update_data["responsavel"] = data["responsavel"]
        if "obra_id" in data and data["obra_id"]:
            try:
                obra_oid = ObjectId(data["obra_id"])
                if not mongo.db.obras.find_one({"_id": obra_oid}):
                    return {"error": "Obra não encontrada"}, 404
                update_data["obra_id"] = obra_oid
            except:
                return {"error": "obra_id inválido"}, 400

        if not update_data:
            return {"error": "Nenhum campo válido para atualizar"}, 400

        mongo.db.gastos.update_one({"_id": oid}, {"$set": update_data})
        return {"message": "Gasto atualizado com sucesso"}

    def delete(self, gasto_id):
        try:
            oid = ObjectId(gasto_id)
        except:
            return {"error": "ID inválido"}, 400

        resultado = mongo.db.gastos.delete_one({"_id": oid})
        if resultado.deleted_count == 0:
            return {"error": "Gasto não encontrado"}, 404

        return {"message": "Gasto deletado com sucesso"}
