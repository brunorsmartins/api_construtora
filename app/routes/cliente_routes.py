from flask_restx import Namespace, Resource, fields
from flask import request, jsonify
from app.db import mongo
from bson import ObjectId

# Define o namespace Swagger
ns = Namespace('clientes', description='Operações relacionadas a clientes')

# Define o modelo de entrada esperado no Swagger
cliente_model = ns.model('Cliente', {
    'nome': fields.String(required=True, description='Nome do cliente'),
    'documento': fields.String(required=True, description='CPF ou CNPJ')
})

@ns.route('/')
class ClienteList(Resource):
    @ns.doc('listar_clientes')
    def get(self):
        """
        Lista todos os clientes cadastrados.
        """
        clientes = mongo.db.clientes.find()
        resultado = []
        for cliente in clientes:
            resultado.append({
                "_id": str(cliente["_id"]),
                "nome": cliente["nome"],
                "documento": cliente["documento"]
            })
        return resultado

    @ns.doc('adicionar_cliente')
    @ns.expect(cliente_model)
    def post(self):
        """
        Adiciona um novo cliente.
        """
        data = request.get_json()

        if not data or not all(k in data for k in ("nome", "documento")):
            return {"error": "Campos 'nome' e 'documento' são obrigatórios."}, 400

        mongo.db.clientes.insert_one({
            "nome": data["nome"],
            "documento": data["documento"]
        })

        return {"message": "Cliente adicionado com sucesso!"}, 201

@ns.route('/<string:cliente_id>')
@ns.param('cliente_id', 'ID do cliente')
class Cliente(Resource):
    @ns.doc('atualizar_cliente')
    @ns.expect(cliente_model, validate=False)
    def put(self, cliente_id):
        """
        Atualiza um cliente pelo ID.
        """
        data = request.get_json()

        try:
            cliente_oid = ObjectId(cliente_id)
        except:
            return {"error": "ID inválido."}, 400

        cliente = mongo.db.clientes.find_one({"_id": cliente_oid})
        if not cliente:
            return {"error": "Cliente não encontrado."}, 404

        update_data = {}
        if "nome" in data:
            update_data["nome"] = data["nome"]
        if "documento" in data:
            update_data["documento"] = data["documento"]

        if not update_data:
            return {"error": "Nenhum campo válido para atualização."}, 400

        mongo.db.clientes.update_one({"_id": cliente_oid}, {"$set": update_data})
        return {"message": "Cliente atualizado com sucesso."}

    @ns.doc('deletar_cliente')
    def delete(self, cliente_id):
        """
        Remove um cliente pelo ID.
        """
        try:
            cliente_oid = ObjectId(cliente_id)
        except:
            return {"error": "ID inválido."}, 400

        resultado = mongo.db.clientes.delete_one({"_id": cliente_oid})
        if resultado.deleted_count == 0:
            return {"error": "Cliente não encontrado."}, 404

        return {"message": "Cliente deletado com sucesso."}
