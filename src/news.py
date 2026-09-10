import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNEWS_API_KEY")


def get_news(company, max_articles=10):

    url = "https://gnews.io/api/v4/search"

    params = {
        "q": f"{company} AND (stock OR revenue OR profit OR earnings OR market OR shares)",
        "lang": "en",
        "max": max_articles,
        "sortby": "publishedAt",
        "apikey": API_KEY
    }

    response = requests.get(url, params=params, timeout=10, verify=False)

    if response.status_code != 200:
        print("News API Error:", response.status_code)
        print(response.text)
        return []

    data = response.json()

    articles = []

    for article in data.get("articles", []):

        articles.append({
            "title": article["title"],
            "source": article["source"]["name"],
            "published": article["publishedAt"],
            "url": article["url"]
        })

    return articles


if __name__ == "__main__":

    articles = get_news("TCS")

    print("\nFinancial News\n")
    print("=" * 80)

    for article in articles:

        print("\nTitle:", article["title"])
        print("Source:", article["source"])
        print("Published:", article["published"])
        print("URL:", article["url"])
        print("-" * 80)