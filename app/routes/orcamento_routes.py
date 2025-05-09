from flask_restx import Namespace, Resource, fields
from flask import request
from app.db import mongo
from bson import ObjectId

ns = Namespace('orcamentos', description='Operações com orçamentos')

orcamento_model = ns.model('Orcamento', {
    'obra_id': fields.String(required=True, description='ID da obra associada'),
    'valor': fields.Float(required=True, description='Valor orçado'),
    'data_orcamento': fields.String(required=True, description='Data do orçamento')
})


@ns.route('/')
class OrcamentoList(Resource):
    @ns.doc('listar_orcamentos')
    def get(self):
        orcs = mongo.db.orcamentos.find()
        resultado = []
        for o in orcs:
            resultado.append({
                "_id": str(o["_id"]),
                "obra_id": str(o["obra_id"]),
                "valor": o["valor"],
                "data_orcamento": o["data_orcamento"]
            })
        return resultado

    @ns.doc('criar_orcamento')
    @ns.expect(orcamento_model)
    def post(self):
        data = request.get_json()

        if not data or not all(k in data for k in ("obra_id", "valor", "data_orcamento")):
            return {"error": "Campos obrigatórios faltando"}, 400

        try:
            obra_oid = ObjectId(data["obra_id"])
        except:
            return {"error": "obra_id inválido"}, 400

        if not mongo.db.obras.find_one({"_id": obra_oid}):
            return {"error": "Obra não encontrada"}, 404

        novo = {
            "obra_id": obra_oid,
            "valor": float(data["valor"]),
            "data_orcamento": data["data_orcamento"]
        }

        mongo.db.orcamentos.insert_one(novo)
        return {"message": "Orçamento criado com sucesso"}, 201



@ns.route('/<string:orcamento_id>')
@ns.param('orcamento_id', 'ID do orçamento')
class Orcamento(Resource):
    def put(self, orcamento_id):
        data = request.get_json()

        try:
            oid = ObjectId(orcamento_id)
        except:
            return {"error": "ID inválido"}, 400

        if not mongo.db.orcamentos.find_one({"_id": oid}):
            return {"error": "Orçamento não encontrado"}, 404

        update_data = {}
        if "valor" in data:
            update_data["valor"] = float(data["valor"])
        if "data_orcamento" in data:
            update_data["data_orcamento"] = data["data_orcamento"]

        if not update_data:
            return {"error": "Nenhum campo para atualizar"}, 400

        mongo.db.orcamentos.update_one({"_id": oid}, {"$set": update_data})
        return {"message": "Orçamento atualizado com sucesso"}

    def delete(self, orcamento_id):
        try:
            oid = ObjectId(orcamento_id)
        except:
            return {"error": "ID inválido"}, 400

        resultado = mongo.db.orcamentos.delete_one({"_id": oid})
        if resultado.deleted_count == 0:
            return {"error": "Orçamento não encontrado"}, 404

        return {"message": "Orçamento deletado com sucesso"}


