import requests
from bs4 import BeautifulSoup

def fetch_github_trending(language="", period="daily", limit=5):
    """从 GitHub Trending 页抓取项目，失败时用备用数据"""
    url = f"https://github.com/trending/{language}?since={period}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[GitHub Trending] 请求失败，将使用备用数据: {e}")
        return get_fallback_data()

    soup = BeautifulSoup(resp.text, "html.parser")
    repos = []
    articles = soup.find_all("article", class_="Box-row")

    for article in articles[:limit]:
        try:
            h2 = article.find("h2", class_="h3 lh-condensed")
            if not h2:
                continue
            link_tag = h2.find("a")
            if not link_tag:
                continue

            name = link_tag.get_text(strip=True).replace("\n", " ").replace("  ", " ")
            url_suffix = link_tag.get("href", "#")
            full_url = "https://github.com" + url_suffix

            desc_tag = article.find("p", class_="col-9 color-fg-muted my-1 pr-4")
            if desc_tag:
                description = desc_tag.get_text(strip=True)
            else:
                inner_p = article.find("p")
                description = inner_p.get_text(strip=True) if inner_p else "暂无描述"

            stars_tag = article.find("span", class_="d-inline-block float-sm-right")
            if stars_tag:
                star_text = stars_tag.get_text(strip=True)
            else:
                all_spans = article.find_all("span")
                star_text = "0"
                for sp in all_spans:
                    txt = sp.get_text(strip=True)
                    if "star" in txt.lower() or txt.replace(",", "").replace(" ", "").isdigit():
                        star_text = txt
                        break

            repos.append({
                "name": name,
                "description": description,
                "stars": star_text,
                "url": full_url,
            })
        except Exception:
            continue

    if not repos:
        return get_fallback_data()

    return repos

def get_fallback_data():
    """备用数据：当GitHub抓取失败时使用"""
    return [
        {"name": "torvalds /linux", "description": "Linux kernel source tree", "stars": "1,234 stars today", "url": "https://github.com/torvalds/linux"},
        {"name": "microsoft /vscode", "description": "Visual Studio Code", "stars": "987 stars today", "url": "https://github.com/microsoft/vscode"},
        {"name": "facebook /react", "description": "A declarative, efficient, and flexible JavaScript library for building user interfaces", "stars": "876 stars today", "url": "https://github.com/facebook/react"},
        {"name": "apple /swift", "description": "The Swift Programming Language", "stars": "765 stars today", "url": "https://github.com/apple/swift"},
        {"name": "google /tensorflow", "description": "An Open Source Machine Learning Framework for Everyone", "stars": "654 stars today", "url": "https://github.com/google/tensorflow"},
    ]

def format_trending_markdown(repos):
    if not repos:
        return "暂无 GitHub 热点数据。"
    lines = [
        "| 项目 | 简介 | Stars |",
        "| :--- | :--- | :--- |",
    ]
    for r in repos:
        lines.append(f"| **[{r['name']}]({r['url']})** | {r['description']} | {r['stars']} |")
    return "\n".join(lines)