import { useContext, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import { AuthContext } from "../context/AuthContext";

export default function Dashboard() {
  const { logout } = useContext(AuthContext);
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [deleteLoading, setDeleteLoading] = useState(false);
  const [deleteError, setDeleteError] = useState("");

  useEffect(() => {
    API.get("/dashboard")
      .then((res) => setData(res.data))
      .catch(() => alert("Unauthorized"));
  }, []);

  if (!data) return <h2 style={{ textAlign: "center" }}>Loading...</h2>;

  const status = String(data.today_status || "unknown").toLowerCase();
  const isSolvedToday =
    status.includes("done") ||
    status.includes("solved") ||
    status.includes("ok") ||
    status.includes("active") ||
    status.includes("yes");

  const storedNames = JSON.parse(
    localStorage.getItem("streakforge_names_by_email") || "{}"
  );
  const emailKey = (data.email || "").toLowerCase();
  const localName = storedNames[emailKey];
  const fallbackName = data.email ? data.email.split("@")[0] : "User";
  const displayName = (localName || fallbackName || "User").trim();

  const handleDeleteAccount = async () => {
    const confirmed = window.confirm(
      "Delete your account permanently? This cannot be undone."
    );

    if (!confirmed) return;

    try {
      setDeleteLoading(true);
      setDeleteError("");
      await API.delete("/delete-account");

      const namesMap = JSON.parse(
        localStorage.getItem("streakforge_names_by_email") || "{}"
      );
      delete namesMap[emailKey];
      localStorage.setItem("streakforge_names_by_email", JSON.stringify(namesMap));

      logout();
      navigate("/signup");
    } catch (error) {
      setDeleteError(
        error.response?.data?.detail || "Failed to delete account"
      );
    } finally {
      setDeleteLoading(false);
    }
  };

  return (
    <div className="page-wrapper dashboard-page">
      <section className="glass dashboard-hero">
        <h1>Welcome back, {displayName} 👋</h1>
        <p>
          Your StreakForge command center: track consistency, see submission
          status, and stay ready for your next coding session.
        </p>
      </section>

      <section className="dashboard-kpi-grid">
        <article className="glass dashboard-kpi">
          <h3>Today's Status</h3>
          <p className={isSolvedToday ? "kpi-value success" : "kpi-value pending"}>
            {data.today_status || "No status"}
          </p>
        </article>
        <article className="glass dashboard-kpi">
          <h3>Last Submission</h3>
          <p className="kpi-value">{data.last_submission_date || "No data"}</p>
        </article>
        <article className="glass dashboard-kpi">
          <h3>Reminder</h3>
          <p className="kpi-value">{data.last_reminder_sent || "Not sent"}</p>
        </article>
        <article className="glass dashboard-kpi">
          <h3>Account Email</h3>
          <p className="kpi-value">{data.email}</p>
        </article>
      </section>

      <section className="dashboard-content-grid">
        <article className="glass dashboard-panel">
          <h2>Today's Plan</h2>
          <ul className="dashboard-list">
            <li>Solve 1 medium problem and review edge cases.</li>
            <li>Revisit one topic from your recent weak area.</li>
            <li>Submit before your daily reminder window.</li>
          </ul>
        </article>

        <article className="glass dashboard-panel">
          <h2>Consistency Insights</h2>
          <p>
            Strong routine comes from small wins. If your status is pending,
            solve one short problem now to keep momentum.
          </p>
          <div className="dashboard-badge-row">
            <span className="dashboard-badge">Focus</span>
            <span className="dashboard-badge">Discipline</span>
            <span className="dashboard-badge">Interview Prep</span>
          </div>
        </article>
      </section>

      <section className="glass dashboard-panel danger-panel">
        <h2>Danger Zone</h2>
        <p>
          Delete your account permanently to stop all StreakForge reminders and
          remove your profile.
        </p>
        <button
          className="btn btn-danger"
          type="button"
          onClick={handleDeleteAccount}
          disabled={deleteLoading}
        >
          {deleteLoading ? "Deleting account..." : "Delete Account Permanently"}
        </button>
        {deleteError && <p className="form-msg error">{deleteError}</p>}
      </section>
    </div>
  );
}