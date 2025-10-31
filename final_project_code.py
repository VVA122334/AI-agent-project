# -*- coding: utf-8 -*-
"""Final project 
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime
try:
    import openai # type: ignore 
    OPENAI_AVAILABLE = True
except ImportError:
    openai = None
    OPENAI_AVAILABLE = False


# Read API keys from environment if available; fall back to in-file values
NEWS_API_KEY = os.environ.get("NEWS_API_KEY", "d804a787bbd44118afd2d2f466c6ae4a")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "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")
if OPENAI_AVAILABLE:
    openai.api_key = OPENAI_API_KEY
else:
    print("Warning: 'openai' package not installed. run: pip install openai")


def latest_news(max_articles: int = 4):
    """ Fetch latest news from NewsAPI using url library.

    Returns a list of articles with keys: title, url, published, and image.
    """
    url = (
        f"https://newsapi.org/v2/everything?q=drone+UAV+DGCA&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    )

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            charset = resp.headers.get_content_charset() or "utf-8"
            data = resp.read().decode(charset)
            news = json.loads(data)
    except urllib.error.HTTPError as e:
        print(f"News API HTTP error: {e.code} {e.reason}")
        return []
    except Exception as e:
        print("Error fetching news:", e)
        return []

    # Debug output (safe): pretty-print JSON if possible
    try:
        print("Full API Response:")
        print(json.dumps(news, indent=2))
    except Exception:
        print(news)

    articles = []
    for n in news.get("articles", [])[:max_articles]:
        articles.append(
            {
                "title": n.get("title"),
                "url": n.get("url"),
                "published": n.get("publishedAt"),
                "image": n.get("urlToImage"),
            }
        )

    return articles


def summarize_article(article: dict) -> str:
    """Send article info to OpenAI and return the assistant's summary text."""
    text = f"Title: {article.get('title')}\nLink: {article.get('url')}"

    # If the openai package is missing, just return a basic fake result so the code doesn’t crash. 
    # During testing, pretend the OpenAI call works by mocking it.
    if not OPENAI_AVAILABLE:
        return f"(OpenAI unavailable) {article.get('title')} - {article.get('url')}"

    # Keep the prompt short; tests should mock this call.
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": text}],
    )

    return response["choices"][0]["message"]["content"]


def format_post(article: dict, summary_text: str) -> str:
    post = f"""
**Drone Industry Update!**

{summary_text}

Read more: {article.get('url')}

#DroneNews #UAV #Technology #IndiaDrones
"""

    return post.strip()


def save_post(post_text: str, article: dict, dest: str = "final_post.json"):
    output = {
        "generated_at": str(datetime.now()),
        "post_text": post_text,
        "image": article.get("image"),
        "title": article.get("title"),
        "article_link": article.get("url"),
    }

    with open(dest, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=4)

    print(f"{dest} saved successfully")


def main():
    print("Finding the latest drone news...")
    articles = latest_news()

    if not articles:
        print("No news found.")
        return

    first_article = articles[0]
    print("Summarizing:", first_article.get("title"))

    summary = summarize_article(first_article)

    print("Formatting social media post...")
    post = format_post(first_article, summary)

    print("Saving final post file...")
    save_post(post, first_article)

    print("\nAutomation completed! Check final_post.json")


if __name__ == "__main__":
    main()



