import { useState } from "react";
import API from "../api/axios";

export default function Support() {
	const [form, setForm] = useState({ name: "", email: "", message: "" });
	const [loading, setLoading] = useState(false);
	const [message, setMessage] = useState("");
	const [error, setError] = useState("");

	const handleSubmit = async (event) => {
		event.preventDefault();
		setLoading(true);
		setMessage("");
		setError("");

		try {
			await API.post("/support-query", form);
			setMessage("Your query has been submitted successfully ✅");
			setForm({ name: "", email: "", message: "" });
		} catch (submitError) {
			setError(submitError.response?.data?.detail || "Failed to submit query");
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="page-wrapper support-bg">
			<section className="glass info-page">
				<h1>Support</h1>
				<p>
					Need help with reminders, account setup, or dashboard usage? Share
					your issue and we’ll help you quickly.
				</p>

				<div className="feature-grid">
					<article className="feature-card">
						<h3>Account Help</h3>
						<p>Problems with signup, login, or profile details.</p>
					</article>
					<article className="feature-card">
						<h3>Reminder Issues</h3>
						<p>Didn’t receive reminder emails or timing looks incorrect.</p>
					</article>
					<article className="feature-card">
						<h3>General Questions</h3>
						<p>Ask anything about features, usage, or workflow best practices.</p>
					</article>
				</div>

				<form className="glass card support-form-card" onSubmit={handleSubmit}>
					<h2>Send a Message</h2>
					<p className="card-subtitle">We usually respond within 24 hours.</p>
					<input
						placeholder="Your name"
						required
						value={form.name}
						onChange={(event) =>
							setForm({ ...form, name: event.target.value })
						}
					/>
					<input
						placeholder="Your email"
						type="email"
						required
						value={form.email}
						onChange={(event) =>
							setForm({ ...form, email: event.target.value })
						}
					/>
					<textarea
						placeholder="Describe your issue"
						required
						value={form.message}
						onChange={(event) =>
							setForm({ ...form, message: event.target.value })
						}
					/>
					<button className="btn btn-primary" type="submit" disabled={loading}>
						{loading ? "Submitting..." : "Submit"}
					</button>
					{message && <p className="form-msg">{message}</p>}
					{error && <p className="form-msg error">{error}</p>}
				</form>
			</section>
		</div>
	);
}
