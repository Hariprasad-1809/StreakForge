import requests
from datetime import datetime
import pytz


def has_submitted_today(leetcode_username: str, timezone: str):
    url = "https://leetcode.com/graphql"

    query = """
    query recentSubmissions($username: String!) {
      recentSubmissionList(username: $username) {
        timestamp
        statusDisplay
      }
    }
    """

    try:
        response = requests.post(
            url,
            json={
                "query": query,
                "variables": {"username": leetcode_username}
            },
            headers={
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            },
            timeout=10
        )
    except Exception as e:
        print("Request failed:", e)
        return False

    if response.status_code != 200:
        print("Status error:", response.status_code)
        return False

    if not response.text.strip():
        print("Empty response")
        return False

    try:
        data = response.json()
    except Exception as e:
        print("JSON decode failed:", e)
        return False

    submissions = data.get("data", {}).get("recentSubmissionList", [])

    today_utc = datetime.utcnow().date()

    for sub in submissions:
        try:
            sub_time_utc = datetime.utcfromtimestamp(int(sub["timestamp"]))
            if (
                sub_time_utc.date() == today_utc
                and sub.get("statusDisplay") == "Accepted"
            ):
                return True
        except:
            continue

    return False


def get_last_submission_date(username: str, timezone: str):
    url = "https://leetcode.com/graphql"

    query = """
    query getRecentSubmissions($username: String!) {
      recentSubmissionList(username: $username) {
        timestamp
      }
    }
    """

    try:
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
    except Exception as e:
        print("Request failed:", e)
        return None

    if response.status_code != 200:
        print("LeetCode API status error:", response.status_code)
        return None

    if not response.text.strip():
        print("Empty response from LeetCode")
        return None

    try:
        data = response.json()
    except Exception as e:
        print("JSON decode failed:", e)
        return None

    submissions = data.get("data", {}).get("recentSubmissionList", [])

    if not submissions:
        return None

    try:
        latest_timestamp = int(submissions[0]["timestamp"])
    except:
        return None

    tz = pytz.timezone(timezone)

    utc_time = datetime.utcfromtimestamp(latest_timestamp).replace(tzinfo=pytz.utc)
    local_time = utc_time.astimezone(tz)

    return local_time
