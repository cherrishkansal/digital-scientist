import google.generativeai as genai
from config import GEMINI_API_KEY
from vector_store import search_similar_papers

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")


def answer_research_question(question):
    similar_papers = search_similar_papers(question, top_k=3)

    context = ""

    for paper in similar_papers:
        context += f"""
Title: {paper['metadata']['title']}
Published: {paper['metadata']['published']}
Link: {paper['metadata']['link']}
Content: {paper['content']}
"""

    if not context:
        return {
            "answer": "No stored research papers found. Run /full-research first to add papers.",
            "sources": []
        }

    prompt = f"""
You are a research assistant.

Answer the user's question using only the research paper context below.

Question:
{question}

Research Context:
{context}

Give:
1. Direct answer
2. Supporting evidence
3. Limitations
"""

    try:
        response = model.generate_content(prompt)
        answer = response.text
    except Exception:
        answer = "Gemini is unavailable right now. Similar research papers were retrieved successfully."

    return {
        "answer": answer,
        "sources": similar_papers
    }