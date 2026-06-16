from hypothesis import generate_hypothesis
from evidence import analyze_evidence
from arxiv_search import search_arxiv
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Digital Scientist API is running"}


@app.get("/research")
def research(claim: str):
    return {
        "claim": claim,
        "status": "Research claim received successfully"
    }

@app.get("/papers")
def get_papers(topic: str):

    papers = search_arxiv(topic)

    return {
        "topic": topic,
        "papers": papers
    }


@app.get("/full-research")
def full_research(claim: str):
    papers = search_arxiv(claim, max_results=2)

    try:
        hypothesis = generate_hypothesis(claim)
        evidence = analyze_evidence(hypothesis, papers)
    except Exception as e:
        hypothesis = "Gemini quota exceeded or unavailable."
        evidence = "AI evidence analysis could not run right now. Research papers were still retrieved successfully."

    return {
        "claim": claim,
        "hypothesis": hypothesis,
        "papers": papers,
        "evidence_analysis": evidence
    }