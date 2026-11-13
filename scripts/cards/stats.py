"""Fetch profile stats from the GitHub GraphQL API -> scripts/cards/stats.json

Needs a token in GITHUB_TOKEN or GH_TOKEN. Login defaults to GITHUB_REPOSITORY_OWNER, then DaniSick.
"""
import datetime as dt
import json
import os
import urllib.request
from theme import HERE

LOGIN = os.environ.get("GITHUB_REPOSITORY_OWNER") or "DaniSick"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
if not TOKEN:
    raise SystemExit("set GITHUB_TOKEN or GH_TOKEN")

QUERY = """query($login: String!) { user(login: $login) {
  createdAt
  followers { totalCount }
  contributionsCollection { contributionCalendar { totalContributions
    weeks { contributionDays { date contributionCount } } } }
} }"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "readme-cards"},
)
with urllib.request.urlopen(req, timeout=30) as r:
    payload = json.load(r)
if payload.get("errors") or not payload.get("data", {}).get("user"):
    raise SystemExit(f"GraphQL error: {payload.get('errors')}")
user = payload["data"]["user"]
cal = user["contributionsCollection"]["contributionCalendar"]
days = sorted((d["date"], d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"])

longest = run = 0
for _, n in days:
    run = run + 1 if n else 0
    longest = max(longest, run)

# Current streak: today may still be empty, so it doesn't break the streak.
today = dt.date.today().isoformat()
counts = [n for d, n in days if d <= today]
if counts and counts[-1] == 0:
    counts.pop()
current = 0
for n in reversed(counts):
    if not n:
        break
    current += 1

stats = {
    "contributions": cal["totalContributions"],
    "current_streak": current,
    "longest_streak": longest,
    "followers": user["followers"]["totalCount"],
    "since": user["createdAt"][:4],
}
with open(os.path.join(HERE, "stats.json"), "w") as f:
    json.dump(stats, f, indent=2)
    f.write("\n")
print(stats)
