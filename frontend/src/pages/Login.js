import { useState, useContext } from "react";
import API from "../api/axios";
import { AuthContext } from "../context/AuthContext";
import { Link, useNavigate } from "react-router-dom";

export default function Login() {
  const { login } = useContext(AuthContext);
  const navigate = useNavigate();

  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");

  const handleLogin = async () => {
    try {
      const res = await API.post("/login", form);
      login(res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      setError("Invalid credentials");
    }
  };

  return (
    <div className="center">
      <div className="glass card">
        <h2>Login</h2>
        <p className="card-subtitle">Welcome back! Continue your coding streak.</p>
        <input
          placeholder="Email"
          type="email"
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />
        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />
        <p className="form-msg">
          <Link to="/forgot-password">Forgot password?</Link>
        </p>
        <button className="btn btn-primary" onClick={handleLogin}>
          Login
        </button>
        {error && <p className="form-msg error">{error}</p>}
        <p className="form-msg">
          New here? <Link to="/signup">Create an account</Link>
        </p>
      </div>
    </div>
  );
}