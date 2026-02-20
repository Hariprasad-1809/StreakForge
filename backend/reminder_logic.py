from leetcode_checker import has_submitted_today


def should_send_reminder(user):
    solved_today = has_submitted_today(
        user.leetcode_username,
        user.timezone
    )

    # If user solved today → NO reminder
    if solved_today:
        return False

    # If not solved → send reminder
    return True
