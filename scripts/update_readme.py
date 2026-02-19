import re
import os
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

def fetch_arxiv_papers():
    url = "https://rss.arxiv.org/rss/cs.LG"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        tree = ET.parse(response)
    root = tree.getroot()
    channel = root.find("channel")
    items = channel.findall("item")[:3]
    papers = []
    for item in items:
        title = item.find("title").text.strip()
        link = item.find("link").text.strip()
        papers.append(f"- [{title}]({link})")
    return "\n".join(papers)

def fetch_github_stats():
    username = "kulharshit21"
    url = f"https://api.github.com/users/{username}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
        import json
        data = json.loads(response.read())
    return (
        f"- 👤 Public Repos: **{data['public_repos']}**\n"
        f"- 👥 Followers: **{data['followers']}**\n"
        f"- ⭐ Following: **{data['following']}**\n"
        f"- 🕒 Last Updated: **{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}**"
    )

def update_section(content, tag, new_content):
    pattern = rf"(<!-- {tag}:START -->)(.*?)(<!-- {tag}:END -->)"
    replacement = rf"\1\n{new_content}\n\3"
    return re.sub(pattern, replacement, content, flags=re.DOTALL)

def main():
    with open("README.md", "r") as f:
        readme = f.read()

    readme = update_section(readme, "ARXIV_PAPERS", fetch_arxiv_papers())
    readme = update_section(readme, "GITHUB_STATS", fetch_github_stats())

    with open("README.md", "w") as f:
        f.write(readme)
    print("README updated successfully!")

if __name__ == "__main__":
    main()
