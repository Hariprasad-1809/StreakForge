import { useState } from "react";
import API from "../api/axios";
import { Link, useNavigate } from "react-router-dom";

export default function Signup() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    password: "",
    leetcode_username: "",
    timezone: "Asia/Kolkata",
  });

  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault(); // 🚨 IMPORTANT

    try {
      setLoading(true);
      setMessage("");

      await API.post("/signup", form);

      const storedNames = JSON.parse(
        localStorage.getItem("streakforge_names_by_email") || "{}"
      );
      localStorage.setItem(
        "streakforge_names_by_email",
        JSON.stringify({
          ...storedNames,
          [form.email.toLowerCase()]: form.name.trim(),
        })
      );

      setMessage("Account created successfully ✅");
      setTimeout(() => navigate("/login"), 1200);

    } catch (err) {
      setMessage(err.response?.data?.detail || "Signup failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="center">
      <form className="glass card" onSubmit={handleSubmit}>
        <h2>Create Account</h2>
        <p className="card-subtitle">Start your daily DSA growth journey.</p>

        <input
          placeholder="Full Name"
          required
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />

        <input
          placeholder="Email"
          type="email"
          required
          onChange={(e) => setForm({ ...form, email: e.target.value })}
        />

        <input
          type="password"
          placeholder="Password"
          required
          onChange={(e) => setForm({ ...form, password: e.target.value })}
        />

        <input
          placeholder="LeetCode Username"
          required
          onChange={(e) =>
            setForm({ ...form, leetcode_username: e.target.value })
          }
        />

        <select
          onChange={(e) =>
            setForm({ ...form, timezone: e.target.value })
          }
        >
          <option value="Asia/Kolkata">Asia/Kolkata</option>
          <option value="America/New_York">America/New_York</option>
          <option value="Europe/London">Europe/London</option>
        </select>

        <button className="btn btn-primary" disabled={loading}>
          {loading ? "Creating..." : "Signup"}
        </button>

        {message && <p className="form-msg">{message}</p>}
        <p className="form-msg">
          Already have an account? <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}