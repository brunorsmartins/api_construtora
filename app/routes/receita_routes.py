from flask_restx import Namespace, Resource, fields
from flask import request
from app.db import mongo
from bson import ObjectId

ns = Namespace('receitas', description='Operações com receitas (pagamentos recebidos)')

receita_model = ns.model('Receita', {
    'obra_id': fields.String(required=True, description='ID da obra'),
    'valor': fields.Float(required=True, description='Valor recebido'),
    'data_recebimento': fields.String(required=True, description='Data do recebimento')
})



@ns.route('/')
class ReceitaList(Resource):
    @ns.doc('listar_receitas')
    def get(self):
        receitas = mongo.db.receitas.find()
        resultado = []
        for r in receitas:
            resultado.append({
                "_id": str(r["_id"]),
                "obra_id": str(r["obra_id"]),
                "valor": r["valor"],
                "data_recebimento": r["data_recebimento"]
            })
        return resultado

    @ns.doc('criar_receita')
    @ns.expect(receita_model)
    def post(self):
        data = request.get_json()

        if not data or not all(k in data for k in ("obra_id", "valor", "data_recebimento")):
            return {"error": "Campos obrigatórios faltando"}, 400

        try:
            obra_oid = ObjectId(data["obra_id"])
        except:
            return {"error": "obra_id inválido"}, 400

        if not mongo.db.obras.find_one({"_id": obra_oid}):
            return {"error": "Obra não encontrada"}, 404

        nova = {
            "obra_id": obra_oid,
            "valor": float(data["valor"]),
            "data_recebimento": data["data_recebimento"]
        }

        mongo.db.receitas.insert_one(nova)
        return {"message": "Receita registrada com sucesso"}, 201


@ns.route('/<string:receita_id>')
@ns.param('receita_id', 'ID da receita')
class Receita(Resource):
    def put(self, receita_id):
        data = request.get_json()

        try:
            oid = ObjectId(receita_id)
        except:
            return {"error": "ID inválido"}, 400

        if not mongo.db.receitas.find_one({"_id": oid}):
            return {"error": "Receita não encontrada"}, 404

        update_data = {}
        if "valor" in data:
            update_data["valor"] = float(data["valor"])
        if "data_recebimento" in data:
            update_data["data_recebimento"] = data["data_recebimento"]

        if not update_data:
            return {"error": "Nenhum campo para atualizar"}, 400

        mongo.db.receitas.update_one({"_id": oid}, {"$set": update_data})
        return {"message": "Receita atualizada com sucesso"}

    def delete(self, receita_id):
        try:
            oid = ObjectId(receita_id)
        except:
            return {"error": "ID inválido"}, 400

        resultado = mongo.db.receitas.delete_one({"_id": oid})
        if resultado.deleted_count == 0:
            return {"error": "Receita não encontrada"}, 404

        return {"message": "Receita deletada com sucesso"}
