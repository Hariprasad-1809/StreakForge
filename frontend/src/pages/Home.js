import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

  return (
    <div className="page-wrapper home-page home-bg">
      <section className="glass hero full-height">
        <h1>Stay Consistent. Stay Ahead.</h1>
        <p>
          Build a stronger DSA habit with daily LeetCode tracking, smart
          reminders, and progress-driven motivation.
        </p>

        <div className="hero-actions">
          <button className="btn btn-primary" onClick={() => navigate("/signup")}>
            Get Started
          </button>
          <button className="btn btn-ghost" onClick={() => navigate("/about")}>
            Learn More
          </button>
        </div>
      </section>

      <section className="feature-grid">
        <article className="feature-card">
          <h3>Daily Reminder Engine</h3>
          <p>Get timely nudges so your coding streak never breaks.</p>
        </article>
        <article className="feature-card">
          <h3>LeetCode Progress Sync</h3>
          <p>Track your solved questions and keep momentum visible.</p>
        </article>
        <article className="feature-card">
          <h3>Simple Dashboard</h3>
          <p>See your status at a glance and stay focused every day.</p>
        </article>
      </section>

      <section className="glass page-section">
        <h2>How Your Daily Flow Works</h2>
        <div className="timeline-grid">
          <article className="timeline-item">
            <h4>1. Set Your LeetCode Username</h4>
            <p>Configure your account once and connect your challenge routine.</p>
          </article>
          <article className="timeline-item">
            <h4>2. Get Smart Reminders</h4>
            <p>Receive nudges based on your schedule and chosen timezone.</p>
          </article>
          <article className="timeline-item">
            <h4>3. Keep the Streak Alive</h4>
            <p>Stay accountable with quick progress checks and consistency cues.</p>
          </article>
          <article className="timeline-item">
            <h4>4. Improve Week by Week</h4>
            <p>Turn short daily sessions into long-term interview readiness.</p>
          </article>
        </div>
      </section>
    </div>
  );
}