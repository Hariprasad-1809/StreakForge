export default function About() {
	return (
		<div className="page-wrapper about-page">
			<section className="glass info-page">
				<h1>About LeetCode Focus</h1>
				<p>
					LeetCode Focus helps you stay consistent with problem solving by
					combining reminder automation with a clean productivity dashboard.
				</p>
				<div className="feature-grid">
					<article className="feature-card">
						<h3>Why We Built It</h3>
						<p>
							Most learners struggle with consistency, not capability. This app
							is built to remove that friction.
						</p>
					</article>
					<article className="feature-card">
						<h3>What You Get</h3>
						<p>
							Personal reminders, streak support, and a simple routine to make
							coding progress sustainable.
						</p>
					</article>
					<article className="feature-card">
						<h3>Who It Is For</h3>
						<p>
							Students, job seekers, and developers preparing for coding
							interviews with a daily plan.
						</p>
					</article>
				</div>
			</section>

			<section className="glass page-section">
				<h2>Our Mission</h2>
				<p>
					We focus on one simple outcome: helping you practice every day. By
					making consistency easier, we help learners build confidence and
					perform better in coding rounds.
				</p>
			</section>

			<section className="glass page-section">
				<h2>What Makes It Different</h2>
				<div className="timeline-grid">
					<article className="timeline-item">
						<h4>Routine First</h4>
						<p>
							The product is built around daily habit support, not one-time
							motivation.
						</p>
					</article>
					<article className="timeline-item">
						<h4>Simple by Design</h4>
						<p>
							Minimal UI keeps you focused on solving problems instead of managing
							complex settings.
						</p>
					</article>
					<article className="timeline-item">
						<h4>Made for Growth</h4>
						<p>
							Every reminder and page exists to support steady progress over time.
						</p>
					</article>
				</div>
			</section>
		</div>
	);
}
