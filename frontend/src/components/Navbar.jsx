import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-gray-800 text-white px-4 py-3 flex justify-between">
      <div className="font-bold text-lg">Empreiteira</div>
      <div className="space-x-4">
        <Link to="/dashboard" className="hover:underline">Dashboard</Link>
        <Link to="/clientes" className="hover:underline">Clientes</Link>
        <Link to="/obras" className="hover:underline">Obras</Link>
        <Link to="/gastos" className="hover:underline">Gastos</Link>
      </div>
    </nav>
  );
};

export default Navbar;
