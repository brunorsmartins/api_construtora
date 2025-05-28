import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Clientes = () => {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');
  const [clientes, setClientes] = useState([]);

  const carregarClientes = async () => {
    try {
      const res = await axios.get('http://localhost:5000/clientes');
      setClientes(res.data);
    } catch (err) {
      console.error('Erro ao buscar clientes:', err);
    }
  };

  useEffect(() => {
    carregarClientes();
  }, []);

  const cadastrar = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/clientes', {
        nome,
        email,
        telefone
      });
      setNome('');
      setEmail('');
      setTelefone('');
      carregarClientes();
    } catch (err) {
      console.error('Erro ao cadastrar cliente:', err);
    }
  };

  const deletarCliente = async (id) => {
    if (!window.confirm('Deseja realmente deletar este cliente?')) return;
    try {
      await axios.delete(`http://localhost:5000/clientes/${id}`);
      setClientes(prev => prev.filter(c => c._id !== id));
    } catch (err) {
      console.error('Erro ao deletar cliente:', err.response?.data || err);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Cadastrar Cliente</h2>
      <form onSubmit={cadastrar} className="space-y-3 mb-6">
        <input
          className="w-full p-2 border rounded"
          placeholder="Nome"
          value={nome}
          onChange={e => setNome(e.target.value)}
          required
        />
        <input
          className="w-full p-2 border rounded"
          placeholder="Email"
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
        <input
          className="w-full p-2 border rounded"
          placeholder="Telefone"
          value={telefone}
          onChange={e => setTelefone(e.target.value)}
          required
        />
        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Salvar
        </button>
      </form>

      <h3 className="text-lg font-semibold mb-2">Clientes Cadastrados</h3>
      <ul className="space-y-1">
        {clientes.map(c => (
          <li
            key={c._id}
            className="flex justify-between items-center border p-2 rounded"
          >
            <div>
              {c.nome} — {c.email} — {c.telefone}
            </div>
            <button
              onClick={() => deletarCliente(c._id)}
              className="text-red-600 hover:underline ml-4"
            >
              Deletar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Clientes;
