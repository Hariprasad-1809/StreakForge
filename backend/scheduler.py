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


import pytz
from leetcode_checker import has_submitted_today
from leetcode_checker import get_last_submission_date
REMINDER_TIMES = ["17:00", "21:00", "23:30"]


def check_users():
    print("🔄 Scheduler running...")

    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"👥 Total users: {len(users)}")

        for user in users:
            try:
                print(f"Checking user: {user.email}")

                # 🌍 User timezone
                user_tz = pytz.timezone(user.timezone)
                now_local = datetime.now(user_tz)

                # ✅ Skip if user solved today
                if has_submitted_today(user.leetcode_username, user.timezone):
                    print("✅ User already solved today")
                    continue

                # 🛑 Prevent duplicate reminder in same slot
                if user.last_reminder_sent:
                    last_local = user.last_reminder_sent.astimezone(user_tz)

                    # If already sent in same hour today, skip
                    if (
                        last_local.date() == now_local.date()
                        and last_local.hour == now_local.hour
                    ):
                        print("⏳ Reminder already sent for this time slot")
                        continue

                print("📧 Sending reminder...")

                # 📩 SAME EMAIL CONTENT (as you requested)
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

                # ⏱ Update last reminder time (UTC stored in DB)
                user.last_reminder_sent = datetime.utcnow()
                db.commit()

                print("✅ Reminder sent successfully")

            except Exception as user_error:
                db.rollback()
                print(f"❌ Reminder failed for {user.email}: {user_error}")

    finally:
        db.close()
def start_scheduler():
    scheduler = BackgroundScheduler(timezone="UTC")

    scheduler.add_job(check_users, "cron", hour=11, minute=30)
    scheduler.add_job(check_users, "cron", hour=15, minute=30)
    scheduler.add_job(check_users, "cron", hour=18, minute=00)

    scheduler.start()
