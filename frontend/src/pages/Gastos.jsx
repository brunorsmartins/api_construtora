import React, { useState, useEffect } from 'react';
import axios from 'axios';

const RESPONSAVEIS = [
  "Marcon Credito", "Marcon PIX", "Marcio PIX",
  "Marcio Credito", "Celso PIX", "Celso Credito", "Bruno PIX"
];

const Gastos = () => {
  const [descricao, setDescricao] = useState('');
  const [valor, setValor]       = useState('');
  const [data, setData]         = useState('');
  const [responsavel, setResponsavel] = useState(RESPONSAVEIS[0]);
  const [obraId, setObraId]     = useState('');
  const [obras, setObras]       = useState([]);
  const [gastos, setGastos]     = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/obras')
      .then(res => setObras(res.data))
      .catch(err => console.error('Erro ao carregar obras:', err));

    carregarGastos();
  }, []);

  const carregarGastos = async () => {
    try {
      const res = await axios.get('http://localhost:5000/gastos');
      setGastos(res.data);
    } catch (err) {
      console.error('Erro ao carregar gastos:', err);
    }
  };

  const cadastrarGasto = async (e) => {
    e.preventDefault();
    try {
      await axios.post('http://localhost:5000/gastos', {
        descricao,
        valor:     parseFloat(valor),
        data,
        responsavel,
        obra_id: obraId || undefined
      });
      // limpa form
      setDescricao('');
      setValor('');
      setData('');
      setResponsavel(RESPONSAVEIS[0]);
      setObraId('');
      // recarrega lista
      await carregarGastos();
    } catch (error) {
      console.error(
        'Erro ao cadastrar gasto:',
        error.response?.data || error
      );
    }
  };

  const deletarGasto = async (id) => {
    if (!window.confirm('Deseja realmente deletar este gasto?')) return;
    try {
      await axios.delete(`http://localhost:5000/gastos/${id}`);
      // atualiza a lista sem o gasto removido
      setGastos(prev => prev.filter(g => g._id !== id));
    } catch (err) {
      console.error('Erro ao deletar gasto:', err.response?.data || err);
    }
  };

  const total = gastos.reduce(
    (acc, g) => acc + (parseFloat(g.valor) || 0),
    0
  );

  return (
    <div className="p-6 max-w-xl mx-auto">
      <h2 className="text-xl font-bold mb-4">Cadastrar Gasto</h2>
      <form onSubmit={cadastrarGasto} className="space-y-3 mb-6">
        <input
          className="w-full p-2 border rounded"
          placeholder="Descrição"
          value={descricao}
          onChange={e => setDescricao(e.target.value)}
          required
        />

        <input
          className="w-full p-2 border rounded"
          placeholder="Valor"
          type="number"
          step="0.01"
          value={valor}
          onChange={e => setValor(e.target.value)}
          required
        />

        <input
          className="w-full p-2 border rounded"
          type="date"
          value={data}
          onChange={e => setData(e.target.value)}
          required
        />

        <select
          className="w-full p-2 border rounded"
          value={responsavel}
          onChange={e => setResponsavel(e.target.value)}
          required
        >
          {RESPONSAVEIS.map(r => (
            <option key={r} value={r}>{r}</option>
          ))}
        </select>

        <select
          className="w-full p-2 border rounded"
          value={obraId}
          onChange={e => setObraId(e.target.value)}
        >
          <option value="">Gasto sem obra</option>
          {obras.map(o => (
            <option key={o._id} value={o._id}>
              {o.nome}
            </option>
          ))}
        </select>

        <button
          type="submit"
          className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        >
          Salvar
        </button>
      </form>

      <h3 className="text-lg font-semibold mb-2">Gastos</h3>
      <ul className="space-y-1">
        {gastos.map(g => (
          <li
            key={g._id}
            className="flex justify-between items-center border p-2 rounded"
          >
            <div>
              {g.descricao} — R${parseFloat(g.valor).toFixed(2)}
              <br/>
              <small>
                {g.data} • {g.responsavel}
                {g.obra_id && <> • Obra: {g.obra_id}</>}
              </small>
            </div>
            <button
              onClick={() => deletarGasto(g._id)}
              className="text-red-600 hover:underline ml-4"
            >
              Deletar
            </button>
          </li>
        ))}
      </ul>

      <div className="mt-4 font-bold">
        Total: R${total.toFixed(2)}
      </div>
    </div>
  );
};

export default Gastos;
