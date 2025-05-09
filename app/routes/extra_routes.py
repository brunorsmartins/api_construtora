from flask_restx import Namespace, Resource, fields
from flask import request
from app.db import mongo
from bson import ObjectId

ns = Namespace('extras', description='Operações com valores extras adicionados a obras')

extra_model = ns.model('Extra', {
    'obra_id': fields.String(required=True, description='ID da obra'),
    'valor': fields.Float(required=True, description='Valor extra'),
    'descricao': fields.String(required=True, description='Motivo ou descrição'),
    'data': fields.String(required=True, description='Data do lançamento')
})


@ns.route('/')
class ExtraList(Resource):
    @ns.doc('listar_extras')
    def get(self):
        extras = mongo.db.extras.find()
        resultado = []
        for e in extras:
            resultado.append({
                "_id": str(e["_id"]),
                "obra_id": str(e["obra_id"]),
                "valor": e["valor"],
                "descricao": e["descricao"],
                "data": e["data"]
            })
        return resultado

    @ns.doc('criar_extra')
    @ns.expect(extra_model)
    def post(self):
        data = request.get_json()

        if not data or not all(k in data for k in ("obra_id", "valor", "descricao", "data")):
            return {"error": "Campos obrigatórios faltando"}, 400

        try:
            obra_oid = ObjectId(data["obra_id"])
        except:
            return {"error": "obra_id inválido"}, 400

        if not mongo.db.obras.find_one({"_id": obra_oid}):
            return {"error": "Obra não encontrada"}, 404

        novo_extra = {
            "obra_id": obra_oid,
            "valor": float(data["valor"]),
            "descricao": data["descricao"],
            "data": data["data"]
        }

        mongo.db.extras.insert_one(novo_extra)
        return {"message": "Extra registrado com sucesso"}, 201


@ns.route('/<string:extra_id>')
@ns.param('extra_id', 'ID do extra')
class Extra(Resource):
    def put(self, extra_id):
        data = request.get_json()

        try:
            oid = ObjectId(extra_id)
        except:
            return {"error": "ID inválido"}, 400

        if not mongo.db.extras.find_one({"_id": oid}):
            return {"error": "Extra não encontrado"}, 404

        update_data = {}
        if "valor" in data:
            update_data["valor"] = float(data["valor"])
        if "descricao" in data:
            update_data["descricao"] = data["descricao"]
        if "data" in data:
            update_data["data"] = data["data"]

        if not update_data:
            return {"error": "Nenhum campo válido para atualizar"}, 400

        mongo.db.extras.update_one({"_id": oid}, {"$set": update_data})
        return {"message": "Extra atualizado com sucesso"}

    def delete(self, extra_id):
        try:
            oid = ObjectId(extra_id)
        except:
            return {"error": "ID inválido"}, 400

        resultado = mongo.db.extras.delete_one({"_id": oid})
        if resultado.deleted_count == 0:
            return {"error": "Extra não encontrado"}, 404

        return {"message": "Extra deletado com sucesso"}
