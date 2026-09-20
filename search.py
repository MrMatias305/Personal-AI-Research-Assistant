import os

import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

def web_search(query, max_results=5):
    url = "https://api.tavily.com/search"

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": max_results,
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()

    data = response.json()

    results = []

    for result in data["results"]:
        results.append({
            "title": result.get("title", ""),
            "url": result.get("url", ""),
            "content": result.get("content", "")
        })

    return results


if __name__ == "__main__":
    results = web_search(query=input("Enter search query: "))

    for index, result in enumerate(results, start=1):
        print(f"\n[{index}] {result['title']}]")
        print(result['url'])
        print(result['content'][:500])