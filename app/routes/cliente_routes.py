# app/routes/cliente_routes.py

from flask import request
from flask_restx import Namespace, Resource, fields
from app.db import mongo
from bson import ObjectId

ns = Namespace('clientes', description='Operações relacionadas a clientes')

cliente_model = ns.model('Cliente', {
    'nome':     fields.String(required=True, description='Nome do cliente'),
    'email':    fields.String(required=True, description='Email do cliente'),
    'telefone': fields.String(required=True, description='Telefone do cliente')
})

@ns.route('/', strict_slashes=False)
class ClienteList(Resource):
    @ns.doc('listar_clientes')
    def get(self):
        clientes = mongo.db.clientes.find()
        resultado = []
        for c in clientes:
            resultado.append({
                "_id":      str(c.get("_id")),
                "nome":     c.get("nome", ""),
                "email":    c.get("email", ""),
                "telefone": c.get("telefone", "")
            })
        return resultado

    @ns.doc('criar_cliente')
    @ns.expect(cliente_model)
    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ("nome", "email", "telefone")):
            return {"error": "Campos obrigatórios faltando"}, 400

        nova = {
            "nome":      data["nome"],
            "email":     data["email"],
            "telefone":  data["telefone"]
        }
        mongo.db.clientes.insert_one(nova)
        return {"message": "Cliente criado com sucesso"}, 201


@ns.route('/<string:cliente_id>', strict_slashes=False)
@ns.param('cliente_id', 'ID do cliente')
class Cliente(Resource):
    def get(self, cliente_id):
        try:
            oid = ObjectId(cliente_id)
        except:
            return {"error": "ID inválido"}, 400

        c = mongo.db.clientes.find_one({"_id": oid})
        if not c:
            return {"error": "Cliente não encontrado"}, 404

        return {
            "_id":      str(c.get("_id")),
            "nome":     c.get("nome", ""),
            "email":    c.get("email", ""),
            "telefone": c.get("telefone", "")
        }

    def put(self, cliente_id):
        data = request.get_json()
        try:
            oid = ObjectId(cliente_id)
        except:
            return {"error": "ID inválido"}, 400

        original = mongo.db.clientes.find_one({"_id": oid})
        if not original:
            return {"error": "Cliente não encontrado"}, 404

        update_data = {}
        for field in ("nome", "email", "telefone"):
            if field in data:
                update_data[field] = data[field]

        if not update_data:
            return {"error": "Nenhum campo válido para atualizar"}, 400

        mongo.db.clientes.update_one({"_id": oid}, {"$set": update_data})
        return {"message": "Cliente atualizado com sucesso"}

    def delete(self, cliente_id):
        try:
            oid = ObjectId(cliente_id)
        except:
            return {"error": "ID inválido"}, 400

        result = mongo.db.clientes.delete_one({"_id": oid})
        if result.deleted_count == 0:
            return {"error": "Cliente não encontrado"}, 404

        return {"message": "Cliente deletado com sucesso"}
