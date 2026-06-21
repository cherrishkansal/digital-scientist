from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os

from hypothesis import generate_hypothesis
from arxiv_search import search_arxiv
from evidence import analyze_evidence
from stats_engine import analyze_dataset
from plot_generator import generate_scatter_plot
from report_generator import generate_report
from pdf_generator import create_pdf_report
from vector_store import add_papers_to_vector_store, search_similar_papers
from research_chat import answer_research_question

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Digital Scientist API is running"}


@app.get("/research")
def research(claim: str):
    try:
        hypothesis = generate_hypothesis(claim)
    except Exception:
        hypothesis = "Gemini quota exceeded or unavailable."

    return {
        "claim": claim,
        "hypothesis": hypothesis
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

    fallback_similar_papers = [
        {
            "content": paper["title"] + " " + paper["summary"],
            "metadata": {
                "title": paper["title"],
                "link": paper["link"],
                "published": paper["published"],
                "similarity_score": "Newly retrieved"
            }
        }
        for paper in papers
    ]

    try:
        add_papers_to_vector_store(papers)
        similar_papers = search_similar_papers(claim, top_k=3)

        if not similar_papers:
            similar_papers = fallback_similar_papers
    except Exception:
        similar_papers = fallback_similar_papers

    try:
        hypothesis = generate_hypothesis(claim)
        evidence = analyze_evidence(hypothesis, papers)

    except Exception as e:
        hypothesis = f"Gemini error: {str(e)}"
        evidence = "AI evidence analysis could not run right now. Research papers were still retrieved successfully."

    return {
        "claim": claim,
        "hypothesis": hypothesis,
        "papers": papers,
        "evidence_analysis": evidence,
        "similar_papers": similar_papers
    }


@app.post("/analyze-dataset")
async def analyze_uploaded_dataset(
    file: UploadFile = File(...),
    independent_col: str = Form(...),
    dependent_col: str = Form(...)
):
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = analyze_dataset(file_path, independent_col, dependent_col)

    plot_path = generate_scatter_plot(
        file_path,
        independent_col,
        dependent_col
    )

    report = generate_report(result)

    pdf_file = create_pdf_report(
        report,
        "research_report.pdf"
    )

    return {
        "filename": file.filename,
        "analysis": result,
        "plot_file": plot_path,
        "research_report": report,
        "pdf_report": pdf_file
    }


@app.get("/research-chat")
def research_chat(question: str):
    return answer_research_question(question)