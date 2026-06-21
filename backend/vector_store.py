import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

STORE_FILE = "vector_papers.json"


def load_store():
    if not os.path.exists(STORE_FILE):
        return []

    with open(STORE_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_store(papers):
    with open(STORE_FILE, "w", encoding="utf-8") as file:
        json.dump(papers, file, indent=4)


def add_papers_to_vector_store(papers):
    stored_papers = load_store()

    existing_titles = {paper["title"] for paper in stored_papers}

    for paper in papers:
        if paper["title"] not in existing_titles:
            stored_papers.append({
                "title": paper["title"],
                "summary": paper["summary"],
                "link": paper["link"],
                "published": paper["published"],
                "content": paper["title"] + " " + paper["summary"]
            })

    save_store(stored_papers)

    return len(papers)


def search_similar_papers(query, top_k=3):
    papers = load_store()

    if not papers:
        return []

    documents = [paper["content"] for paper in papers]

    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform(documents + [query])

    similarities = cosine_similarity(vectors[-1], vectors[:-1]).flatten()

    top_indexes = similarities.argsort()[-top_k:][::-1]

    results = []

    for index in top_indexes:
        paper = papers[index]

        results.append({
            "content": paper["content"],
            "metadata": {
                "title": paper["title"],
                "link": paper["link"],
                "published": paper["published"],
                "similarity_score": round(float(similarities[index]), 4)
            }
        })

    return results