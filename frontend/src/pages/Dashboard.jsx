import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
  const [clientes, setClientes] = useState([]);
  const [obras, setObras] = useState([]);
  const [gastos, setGastos] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/clientes').then(res => setClientes(res.data));
    axios.get('http://localhost:5000/obras').then(res => setObras(res.data));
    axios.get('http://localhost:5000/gastos').then(res => setGastos(res.data));
  }, []);

  const totalGastos = gastos.reduce((soma, g) => soma + (parseFloat(g.valor) || 0), 0);

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <h1 className="text-2xl font-bold mb-6">Dashboard</h1>
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
        <div className="bg-white shadow rounded p-4 text-center">
          <h2 className="text-xl font-semibold">Clientes</h2>
          <p className="text-3xl mt-2">{clientes.length}</p>
        </div>
        <div className="bg-white shadow rounded p-4 text-center">
          <h2 className="text-xl font-semibold">Obras</h2>
          <p className="text-3xl mt-2">{obras.length}</p>
        </div>
        <div className="bg-white shadow rounded p-4 text-center">
          <h2 className="text-xl font-semibold">Total de Gastos</h2>
          <p className="text-3xl mt-2 text-red-600">R$ {totalGastos.toFixed(2)}</p>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
