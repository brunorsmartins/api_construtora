import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Dashboard from './pages/Dashboard';
import Clientes from './pages/Clientes';
import Obras from './pages/Obras';
import ObraDetalhe from './pages/ObraDetalhe';
import Gastos from './pages/Gastos';
import Login from './pages/Login';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/clientes" element={<Clientes />} />
        <Route path="/obras" element={<Obras />} />
        <Route path="/obras/:id" element={<ObraDetalhe/>} />
        <Route path="/gastos" element={<Gastos />} />
      </Routes>
    </Router>
  );
}

export default App;
