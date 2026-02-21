import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api/axios";

export default function ForgotPassword() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    email: "",
    code: "",
    new_password: "",
  });
  const [loadingCode, setLoadingCode] = useState(false);
  const [loadingReset, setLoadingReset] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const requestCode = async () => {
    try {
      setLoadingCode(true);
      setMessage("");
      setError("");

      await API.post("/forgot-password", { email: form.email });
      setMessage("Reset code sent to your email.");
    } catch (requestError) {
      setError(requestError.response?.data?.detail || "Failed to send reset code");
    } finally {
      setLoadingCode(false);
    }
  };

  const handleReset = async (event) => {
    event.preventDefault();
    try {
      setLoadingReset(true);
      setMessage("");
      setError("");

      await API.post("/reset-password", {
        email: form.email,
        code: form.code,
        new_password: form.new_password,
      });

      setMessage("Password reset successful ✅ Redirecting to login...");
      setTimeout(() => navigate("/login"), 1200);
    } catch (resetError) {
      setError(resetError.response?.data?.detail || "Failed to reset password");
    } finally {
      setLoadingReset(false);
    }
  };

  return (
    <div className="center">
      <form className="glass card" onSubmit={handleReset}>
        <h2>Forgot Password</h2>
        <p className="card-subtitle">Request a code and reset your password securely.</p>

        <input
          type="email"
          placeholder="Your email"
          required
          value={form.email}
          onChange={(event) => setForm({ ...form, email: event.target.value })}
        />

        <button
          className="btn btn-ghost"
          type="button"
          disabled={loadingCode || !form.email}
          onClick={requestCode}
        >
          {loadingCode ? "Sending code..." : "Send Reset Code"}
        </button>

        <input
          placeholder="Enter 6-digit code"
          required
          value={form.code}
          onChange={(event) => setForm({ ...form, code: event.target.value })}
        />

        <input
          type="password"
          placeholder="New password"
          required
          value={form.new_password}
          onChange={(event) =>
            setForm({ ...form, new_password: event.target.value })
          }
        />

        <button className="btn btn-primary" type="submit" disabled={loadingReset}>
          {loadingReset ? "Resetting..." : "Reset Password"}
        </button>

        {message && <p className="form-msg">{message}</p>}
        {error && <p className="form-msg error">{error}</p>}

        <p className="form-msg">
          Back to <Link to="/login">Login</Link>
        </p>
      </form>
    </div>
  );
}