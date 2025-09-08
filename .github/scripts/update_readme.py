import requests
import re

USERNAME = "XreeceX"   # your GitHub username
THEME = "radical"      # theme for repo cards
MAX_REPOS = 20         # max repos to display
REPOS_PER_ROW = 2      # number of cards per row

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?per_page=100&sort=updated"
    repos = []
    while url:
        response = requests.get(url)
        response.raise_for_status()
        repos.extend(response.json())
        url = response.links.get("next", {}).get("url")
    return repos

def generate_cards(repos):
    cards = []
    row = []
    for i, repo in enumerate(repos[:MAX_REPOS], start=1):
        name = repo["name"]
        row.append(f"![Repo Card](https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&theme={THEME})")
        if i % REPOS_PER_ROW == 0:
            cards.append(" ".join(row))
            row = []
    if row:
        cards.append(" ".join(row))  # last row
    # Add "See more" link
    cards.append(f"\n👉 [See all repositories](https://github.com/{USERNAME}?tab=repositories)\n")
    return "\n\n".join(cards)

def update_readme(new_cards):
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()

    new_readme = re.sub(
        r"<!--START_SECTION:repos-->[\s\S]*<!--END_SECTION:repos-->",
        f"<!--START_SECTION:repos-->\n{new_cards}\n<!--END_SECTION:repos-->",
        readme,
    )

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    repos = fetch_repos(USERNAME)
    cards = generate_cards(repos)
    update_readme(cards)
