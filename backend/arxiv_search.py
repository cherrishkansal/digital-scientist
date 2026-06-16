import requests
import feedparser
from urllib.parse import quote


def search_arxiv(query, max_results=5):

    encoded_query = quote(query)

    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{encoded_query}"
        f"&start=0"
        f"&max_results={max_results}"
    )

    response = requests.get(url)

    feed = feedparser.parse(response.text)

    papers = []

    for entry in feed.entries:

        papers.append({
            "title": entry.title,
            "summary": entry.summary[:500],
            "published": entry.published,
            "link": entry.link
        })

    return papers