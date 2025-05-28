import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';
import { auth } from '../firebase';

const Login = () => {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');
  const navigate = useNavigate();

  const fazerLogin = async (e) => {
    e.preventDefault();
    try {
      await signInWithEmailAndPassword(auth, email, senha);
      navigate('/dashboard');
    } catch (error) {
      setErro('Email ou senha inválidos');
    }
  };

  return (
    <div className="p-6 max-w-sm mx-auto">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      <form onSubmit={fazerLogin} className="space-y-4">
        <input type="email" placeholder="Email" className="w-full border p-2 rounded" value={email} onChange={e => setEmail(e.target.value)} required />
        <input type="password" placeholder="Senha" className="w-full border p-2 rounded" value={senha} onChange={e => setSenha(e.target.value)} required />
        <button type="submit" className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700">Entrar</button>
      </form>
      {erro && <p className="text-red-600 mt-2">{erro}</p>}
    </div>
  );
};

export default Login;
