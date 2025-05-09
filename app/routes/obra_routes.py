from flask import request, jsonify
from flask_restx import Namespace, Resource, fields
from app.db import mongo
from bson import ObjectId

ns = Namespace('obras', description='Operações com obras')

obra_model = ns.model('Obra', {
    'cliente_id': fields.String(required=True, description='ID do cliente'),
    'nome': fields.String(required=True, description='Nome da obra'),
    'data_inicio': fields.String(required=True, description='Data de início'),
    'status': fields.String(required=True, description='Status da obra (ex: ATIVA, FINALIZADA)')
})

@ns.route('/')
class ObraList(Resource):
    @ns.doc('listar_obras')
    def get(self):
        obras = mongo.db.obras.find()
        resultado = []
        for obra in obras:
            resultado.append({
                "_id": str(obra["_id"]),
                "cliente_id": str(obra["cliente_id"]),
                "nome": obra["nome"],
                "data_inicio": obra["data_inicio"],
                "status": obra["status"]
            })
        return resultado

    @ns.doc('criar_obra')
    @ns.expect(obra_model)
    def post(self):
        data = request.get_json()

        if not data or not all(k in data for k in ("cliente_id", "nome", "data_inicio", "status")):
            return {"error": "Campos obrigatórios faltando"}, 400

        try:
            cliente_oid = ObjectId(data["cliente_id"])
        except:
            return {"error": "cliente_id inválido"}, 400

        if not mongo.db.clientes.find_one({"_id": cliente_oid}):
            return {"error": "Cliente não encontrado"}, 404

        nova_obra = {
            "cliente_id": cliente_oid,
            "nome": data["nome"],
            "data_inicio": data["data_inicio"],
            "status": data["status"]
        }

        mongo.db.obras.insert_one(nova_obra)
        return {"message": "Obra criada com sucesso"}, 201

@ns.route('/<string:obra_id>')
@ns.param('obra_id', 'ID da obra')
class Obra(Resource):
    def put(self, obra_id):
        data = request.get_json()

        try:
            obra_oid = ObjectId(obra_id)
        except:
            return {"error": "ID inválido"}, 400

        obra = mongo.db.obras.find_one({"_id": obra_oid})
        if not obra:
            return {"error": "Obra não encontrada"}, 404

        update_data = {}
        for campo in ("nome", "data_inicio", "status"):
            if campo in data:
                update_data[campo] = data[campo]

        if not update_data:
            return {"error": "Nenhum campo válido"}, 400

        mongo.db.obras.update_one({"_id": obra_oid}, {"$set": update_data})
        return {"message": "Obra atualizada com sucesso"}

    def delete(self, obra_id):
        try:
            obra_oid = ObjectId(obra_id)
        except:
            return {"error": "ID inválido"}, 400

        resultado = mongo.db.obras.delete_one({"_id": obra_oid})
        if resultado.deleted_count == 0:
            return {"error": "Obra não encontrada"}, 404

        return {"message": "Obra deletada com sucesso"}
