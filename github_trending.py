import requests
from bs4 import BeautifulSoup

def fetch_github_trending(language="", period="daily", limit=5):
    url = f"https://github.com/trending/{language}?since={period}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
    }
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[GitHub Trending] 请求失败: {e}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    repos = []
    articles = soup.find_all("article", class_="Box-row")

    for article in articles[:limit]:
        try:
            h2 = article.find("h2", class_="h3 lh-condensed")
            name_link = h2.find("a") if h2 else None
            name = name_link.get_text(strip=True).replace("\n", " ").replace("  ", " ") if name_link else "?"
            url_suffix = name_link["href"] if name_link else "#"
            full_url = "https://github.com" + url_suffix

            desc_p = article.find("p", class_="col-9 color-fg-muted my-1 pr-4")
            description = desc_p.get_text(strip=True) if desc_p else "无描述"

            stars_span = article.find("span", class_="d-inline-block float-sm-right")
            star_text = stars_span.get_text(strip=True) if stars_span else "0"
            repos.append({
                "name": name,
                "description": description,
                "stars": star_text,
                "url": full_url,
            })
        except Exception:
            continue

    return repos

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