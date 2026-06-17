from fastapi import FastAPI, UploadFile, File, Form
import shutil
import os
from stats_engine import analyze_dataset
from hypothesis import generate_hypothesis
from evidence import analyze_evidence
from arxiv_search import search_arxiv


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

    return {
        "filename": file.filename,
        "analysis": result
    }