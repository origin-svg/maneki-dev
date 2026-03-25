import requests
import os

# Repository settings
REPO_OWNER = "origin-svg"
REPO_NAME = "maneki-dev"

# Fetch releases from GitHub API
url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
resp = requests.get(url)
releases = resp.json()

# Calculate total downloads across all assets
total_downloads = sum(
    asset['download_count'] for release in releases for asset in release['assets']
)

# Gamification rules
points = total_downloads // 100
badge = "🏆" if total_downloads >= 1000 else "🎖️"

# Output Markdown file
GAMIFICATION_FILE = "GAMIFICATION.md"
with open(GAMIFICATION_FILE, "w", encoding="utf-8") as f:
    f.write("# Gamification Stats\n\n")
    f.write(f"**Total Downloads:** {total_downloads}\n")
    f.write(f"**Points Earned:** {points}\n")
    f.write(f"**Badge:** {badge}\n")

print(f"GAMIFICATION.md updated! Total downloads: {total_downloads}, Points: {points}, Badge: {badge}")
