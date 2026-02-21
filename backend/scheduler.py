from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
try:
    from .database import SessionLocal
    from .models import User
    from .reminder_logic import should_send_reminder
    from .email_utils import send_email
except ImportError:
    from database import SessionLocal
    from models import User
    from reminder_logic import should_send_reminder
    from email_utils import send_email

from datetime import datetime, timedelta


def check_users():
    print("🔄 Scheduler running...")

    db = SessionLocal()
    try:
        users = db.query(User).all()

        print(f"👥 Total users: {len(users)}")

        for user in users:
            try:
                print(f"Checking user: {user.email}")

                now = datetime.utcnow()

                if not should_send_reminder(user):
                    print("✅ No reminder needed")
                    continue

                if user.last_reminder_sent:
                    if now - user.last_reminder_sent < timedelta(hours=6):
                        print("⏳ Reminder already sent recently")
                        continue

                print("📧 Sending reminder...")

                send_email(
                    to_email=user.email,
                    subject="🚀 LeetCode Reminder",
                    body=(
                        "👋 Hi Coder, this is your StreakForge reminder!\n"
                        "🔥 One problem a day keeps your momentum alive.\n"
                        "🧠 Consistency beats intensity in coding success.\n"
                        "✅ Solve at least one DSA problem today.\n"
                        "⏳ If you skip today, your streak can break.\n"
                        "💪 Show up now — even 20 minutes is enough.\n"
                        "🏆 Small daily wins create big interview results.\n"
                        "🚀 Keep going, you are building a strong future!\n\n"
                        "—Hariprasad H\n"
                        "StreakForge"
                    )
                )

                user.last_reminder_sent = now
                db.commit()
                print("✅ Reminder sent")
            except Exception as user_error:
                db.rollback()
                print(f"❌ Reminder failed for {user.email}: {user_error}")
    finally:
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
