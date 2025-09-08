import requests
import re

USERNAME = "XreeceX"   # your GitHub username
THEME = "radical"      # theme for repo cards
MAX_REPOS = 6          # number of repos to show

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos?sort=updated"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def generate_cards(repos):
    cards = []
    for repo in repos[:MAX_REPOS]:
        name = repo["name"]
        cards.append(f"![Repo Card](https://github-readme-stats.vercel.app/api/pin/?username={USERNAME}&repo={name}&theme={THEME})")
    return "\n".join(cards)

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
