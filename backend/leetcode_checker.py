from datetime import datetime
import pytz

# TEMPORARY MOCK FUNCTION
# Later you can connect real LeetCode API
def has_submitted_today(leetcode_username, timezone):
    import requests
    from datetime import datetime
    import pytz

    url = "https://leetcode.com/graphql"

    query = """
    query recentSubmissions($username: String!) {
      recentSubmissionList(username: $username) {
        timestamp
        statusDisplay
      }
    }
    """

    variables = {"username": leetcode_username}

    response = requests.post(
        url,
        json={"query": query, "variables": variables}
    )

    if response.status_code != 200:
        return False

    data = response.json()
    submissions = data["data"]["recentSubmissionList"]

    # 🔥 IMPORTANT: Use UTC date (LeetCode logic)
    today_utc = datetime.utcnow().date()

    for sub in submissions:
        sub_time_utc = datetime.utcfromtimestamp(int(sub["timestamp"]))

        if (
            sub_time_utc.date() == today_utc
            and sub["statusDisplay"] == "Accepted"
        ):
            return True

    return False

import requests
from datetime import datetime
import pytz

def get_last_submission_date(username: str, timezone: str):
    url = f"https://leetcode.com/graphql"

    query = """
    query getRecentSubmissions($username: String!) {
      recentSubmissionList(username: $username) {
        timestamp
      }
    }
    """

    response = requests.post(
    url,
    json={
        "query": query,
        "variables": {"username": username}
    },
    headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0"
    },
    timeout=10
)

# ---- SAFE RESPONSE HANDLING ----

if response.status_code != 200:
    print("LeetCode API status error:", response.status_code)
    print("Response:", response.text)
    return None

    if not response.text.strip():
        print("Empty response from LeetCode")
        return None

    try:
        data = response.json()
    except Exception as e:
        print("JSON decode failed:", e)
        print("Raw response:", response.text)
        return None

    submissions = data.get("data", {}).get("recentSubmissionList", [])

    if not submissions:
        return None

    latest_timestamp = int(submissions[0]["timestamp"])

    tz = pytz.timezone(timezone)

    utc_time = datetime.utcfromtimestamp(latest_timestamp).replace(tzinfo=pytz.utc)
    local_time = utc_time.astimezone(tz)

    return local_time
