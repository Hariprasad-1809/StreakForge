from apscheduler.schedulers.background import BackgroundScheduler
from database import SessionLocal
from models import User
from reminder_logic import should_send_reminder
from email_utils import send_email
from datetime import datetime, timedelta


def check_users():
    print("🔄 Scheduler running...")

    db = SessionLocal()
    users = db.query(User).all()

    print(f"👥 Total users: {len(users)}")

    for user in users:
        print(f"Checking user: {user.email}")

        # Use naive datetime everywhere
        now = datetime.utcnow()

        if not should_send_reminder(user):
            print("✅ No reminder needed")
            continue

        # 6-hour cooldown
        if user.last_reminder_sent:
            if now - user.last_reminder_sent < timedelta(hours=6):
                print("⏳ Reminder already sent recently")
                continue

        print("📧 Sending reminder...")

        send_email(
            to_email=user.email,
            subject="🚀 LeetCode Reminder",
            body="You haven't solved a problem today. Keep your streak alive!"
        )

        user.last_reminder_sent = now
        db.commit()

    db.close()


def start_scheduler():
    scheduler = BackgroundScheduler()

    scheduler.add_job(
        check_users,
        "interval",
        minutes=1,
        max_instances=3,      # allow parallel runs
        coalesce=True         # merge skipped runs
    )

    scheduler.start()