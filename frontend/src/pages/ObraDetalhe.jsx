// src/pages/ObraDetalhe.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams, Link } from 'react-router-dom';

const RESPONSAVEIS = [
  "Marcon Credito", "Marcon PIX", "Marcio PIX",
  "Marcio Credito", "Celso PIX", "Celso Credito", "Bruno PIX"
];

const ObraDetalhe = () => {
  const { id } = useParams();
  const [obra, setObra] = useState(null);
  const [gastos, setGastos] = useState([]);

  // edição de status
  const [editStatus, setEditStatus] = useState(false);
  const [newStatus, setNewStatus] = useState('');

  // estados para edição inline de gastos
  const [editGastoId, setEditGastoId] = useState(null);
  const [editDescricao, setEditDescricao] = useState('');
  const [editValor, setEditValor] = useState('');
  const [editData, setEditData] = useState('');
  const [editResponsavel, setEditResponsavel] = useState(RESPONSAVEIS[0]);

  // carrega obra
  const carregarObra = async () => {
    try {
      const res = await axios.get(`http://localhost:5000/obras/${id}`);
      setObra(res.data);
      setNewStatus(res.data.status);
    } catch (err) {
      console.error('Erro ao carregar obra:', err);
    }
  };

  // carrega gastos da obra
  const carregarGastos = async () => {
    try {
      const res = await axios.get('http://localhost:5000/gastos');
      setGastos(res.data.filter(g => g.obra_id === id));
    } catch (err) {
      console.error('Erro ao carregar gastos:', err);
    }
  };

  useEffect(() => {
    carregarObra();
    carregarGastos();
  }, [id]);

  // enviar PUT para atualizar status
  const salvarStatus = async () => {
    try {
      await axios.put(
  `http://localhost:5000/obras/${id}`,
  { status: newStatus }
);
      setObra(prev => ({ ...prev, status: newStatus }));
      setEditStatus(false);
    } catch (err) {
      console.error('Erro ao atualizar status:', err.response?.data || err);
    }
  };

  // inicia edição de gasto
  const iniciarEdicao = (g) => {
    setEditGastoId(g._id);
    setEditDescricao(g.descricao);
    setEditValor(g.valor);
    setEditData(g.data);
    setEditResponsavel(g.responsavel);
  };

  // salva edição de gasto
  const salvarEdicao = async (gastoId) => {
    try {
      await axios.put(`http://localhost:5000/gastos/${gastoId}`, {
        descricao: editDescricao,
        valor: parseFloat(editValor),
        data: editData,
        responsavel: editResponsavel,
        obra_id: id
      });
      setGastos(prev =>
        prev.map(g =>
          g._id === gastoId
            ? { ...g, descricao: editDescricao, valor: editValor, data: editData, responsavel: editResponsavel }
            : g
        )
      );
      setEditGastoId(null);
    } catch (err) {
      console.error('Erro ao atualizar gasto:', err.response?.data || err);
    }
  };

  // cancelar edição de gasto
  const cancelarEdicao = () => setEditGastoId(null);

  // deletar gasto
  const deletarGasto = async (gastoId) => {
    if (!window.confirm('Deseja realmente deletar este gasto?')) return;
    try {
      await axios.delete(`http://localhost:5000/gastos/${gastoId}`);
      setGastos(prev => prev.filter(g => g._id !== gastoId));
    } catch (err) {
      console.error('Erro ao deletar gasto:', err.response?.data || err);
    }
  };

  if (!obra) return <div>Carregando detalhes da obra...</div>;

  // agrupa total por responsável
  const totalPorResponsavel = gastos.reduce((acc, g) => {
    acc[g.responsavel] = (acc[g.responsavel] || 0) + parseFloat(g.valor);
    return acc;
  }, {});

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <Link to="/obras" className="text-blue-600 hover:underline mb-4 inline-block">
        ← Voltar às Obras
      </Link>

      <h2 className="text-2xl font-bold mb-2">{obra.nome}</h2>

      {/* Edição de status */}
      <div className="mb-6 flex items-center space-x-2">
        {editStatus ? (
          <>
            <select
              className="p-2 border rounded"
              value={newStatus}
              onChange={e => setNewStatus(e.target.value)}
            >
              <option value="ATIVA">ATIVA</option>
              <option value="FINALIZADA">FINALIZADA</option>
            </select>
            <button
              className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
              onClick={salvarStatus}
            >
              Salvar
            </button>
            <button
              className="bg-gray-400 text-white px-3 py-1 rounded hover:bg-gray-500"
              onClick={() => { setNewStatus(obra.status); setEditStatus(false); }}
            >
              Cancelar
            </button>
          </>
        ) : (
          <>
            <span className="font-semibold">Status:</span>
            <span>{obra.status}</span>
            <button
              className="text-blue-600 hover:underline ml-2"
              onClick={() => setEditStatus(true)}
            >
              Editar
            </button>
          </>
        )}
      </div>

      <h3 className="text-xl font-semibold mb-2">Gastos desta Obra</h3>
      <ul className="space-y-4 mb-6">
        {gastos.length === 0 && (
          <li className="text-gray-600">Nenhum gasto cadastrado.</li>
        )}
        {gastos.map(g => (
          <li key={g._id} className="border p-4 rounded">
            {editGastoId === g._id ? (
              <div className="space-y-2">
                <input
                  className="w-full p-2 border rounded"
                  value={editDescricao}
                  onChange={e => setEditDescricao(e.target.value)}
                />
                <input
                  className="w-full p-2 border rounded"
                  type="number"
                  step="0.01"
                  value={editValor}
                  onChange={e => setEditValor(e.target.value)}
                />
                <input
                  className="w-full p-2 border rounded"
                  type="date"
                  value={editData}
                  onChange={e => setEditData(e.target.value)}
                />
                <select
                  className="w-full p-2 border rounded"
                  value={editResponsavel}
                  onChange={e => setEditResponsavel(e.target.value)}
                >
                  {RESPONSAVEIS.map(r => (
                    <option key={r} value={r}>{r}</option>
                  ))}
                </select>
                <div className="flex space-x-2">
                  <button
                    className="bg-green-600 text-white px-4 py-2 rounded hover:bg-green-700"
                    onClick={() => salvarEdicao(g._id)}
                  >
                    Salvar
                  </button>
                  <button
                    className="bg-gray-400 text-white px-4 py-2 rounded hover:bg-gray-500"
                    onClick={cancelarEdicao}
                  >
                    Cancelar
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex justify-between items-start">
                <div>
                  <div>{g.data} — {g.descricao}</div>
                  <div className="text-sm text-gray-600">
                    R${parseFloat(g.valor).toFixed(2)} • {g.responsavel}
                  </div>
                </div>
                <div className="flex space-x-4">
                  <button
                    className="text-blue-600 hover:underline"
                    onClick={() => iniciarEdicao(g)}
                  >
                    Editar
                  </button>
                  <button
                    className="text-red-600 hover:underline"
                    onClick={() => deletarGasto(g._id)}
                  >
                    Deletar
                  </button>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>

      <h3 className="text-xl font-semibold mb-2">Total por Responsável</h3>
      <ul className="space-y-1">
        {Object.entries(totalPorResponsavel).map(([resp, tot]) => (
          <li key={resp} className="border p-2 rounded">
            {resp}: R${tot.toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ObraDetalhe;
