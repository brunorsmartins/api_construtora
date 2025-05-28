import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const Obras = () => {
  const [nome, setNome] = useState('');
  const [descricao, setDescricao] = useState('');
  const [inicio, setInicio] = useState('');
  const [status, setStatus] = useState('ATIVA');
  const [clienteId, setClienteId] = useState('');
  const [clientes, setClientes] = useState([]);
  const [obras, setObras] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/clientes')
      .then(res => setClientes(res.data))
      .catch(err => console.error('Erro ao carregar clientes:', err));

    carregarObras();
  }, []);

  const carregarObras = async () => {
    try {
      const res = await axios.get('http://localhost:5000/obras');
      setObras(res.data);
    } catch (err) {
      console.error('Erro ao carregar obras:', err);
    }
  };

  const cadastrarObra = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/obras', {
        nome,
        descricao,
        data_inicio: inicio,
        cliente_id: clienteId,
        status
      });
      setNome('');
      setDescricao('');
      setInicio('');
      setStatus('ATIVA');
      setClienteId('');
      await carregarObras();
    } catch (error) {
      console.error('Erro ao cadastrar obra:', error.response?.data || error);
    }
  };

  const deletarObra = async (id) => {
    if (!window.confirm('Deseja realmente deletar esta obra?')) return;
    try {
      await axios.delete(`http://localhost:5000/obras/${id}`);
      setObras(prev => prev.filter(o => o._id !== id));
    } catch (err) {
      console.error('Erro ao deletar obra:', err.response?.data || err);
    }
  };

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Cadastrar Obra</h2>

      <form onSubmit={cadastrarObra} className="space-y-3 mb-6">
        <input
          className="w-full p-2 border rounded"
          placeholder="Nome da obra"
          value={nome}
          onChange={e => setNome(e.target.value)}
          required
        />

        <textarea
          className="w-full p-2 border rounded"
          placeholder="Descrição"
          value={descricao}
          onChange={e => setDescricao(e.target.value)}
          required
        />

        <input
          className="w-full p-2 border rounded"
          type="date"
          value={inicio}
          onChange={e => setInicio(e.target.value)}
          required
        />

        <select
          className="w-full p-2 border rounded"
          value={status}
          onChange={e => setStatus(e.target.value)}
          required
        >
          <option value="ATIVA">ATIVA</option>
          <option value="FINALIZADA">FINALIZADA</option>
        </select>

        <select
          className="w-full p-2 border rounded"
          value={clienteId}
          onChange={e => setClienteId(e.target.value)}
          required
        >
          <option value="">Selecione um Cliente</option>
          {clientes.map(cli => (
            <option key={cli._id} value={cli._id}>
              {cli.nome}
            </option>
          ))}
        </select>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Cadastrar
        </button>
      </form>

      <h3 className="text-lg font-semibold mb-2">Obras Cadastradas</h3>
      <ul className="space-y-1">
        {obras.map(obra => (
          <li
            key={obra._id}
            className="flex justify-between items-center border p-2 rounded"
          >
            <Link
              to={`/obras/${obra._id}`}
              className="flex-1 text-blue-600 hover:underline"
            >
              <strong>{obra.nome}</strong> — {obra.descricao} ({obra.status})
            </Link>
            <button
              onClick={() => deletarObra(obra._id)}
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

export default Obras;
