# Digital Scientist

Digital Scientist is an AI-powered research assistant that converts natural-language claims into research hypotheses, retrieves academic papers, performs evidence analysis, validates uploaded datasets statistically, generates visualizations, and creates PDF research reports.

## Features

* AI-based hypothesis generation
* arXiv academic paper search
* Evidence analysis using Gemini
* Vector-based similar paper retrieval
* Research Chat using stored papers
* RAG-style question answering
* CSV dataset upload
* Pearson correlation analysis
* P-value calculation
* Statistical significance detection
* Scatter plot generation
* PDF research report generation
* Streamlit dashboard
* FastAPI backend

## Tech Stack

* Python
* FastAPI
* Streamlit
* Gemini API
* arXiv API
* Pandas
* SciPy
* Scikit-learn
* Matplotlib
* ReportLab
* Git and GitHub

## Project Architecture

```text
User
 ↓
Streamlit Dashboard
 ↓
FastAPI Backend
 ↓
Gemini API / arXiv API / Statistical Engine / Vector Search
 ↓
Hypothesis + Papers + Similar Papers + Research Chat + PDF Report
```

## Main Modules

```text
backend/
├── main.py
├── hypothesis.py
├── arxiv_search.py
├── evidence.py
├── stats_engine.py
├── plot_generator.py
├── report_generator.py
├── pdf_generator.py
├── vector_store.py
├── research_chat.py
└── frontend.py
```

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/cherrishkansal/digital-scientist.git
cd digital-scientist/backend
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r ../requirements.txt
```

### 4. Add Gemini API key

Create a `.env` file inside `backend`:

```env
GEMINI_API_KEY=your_api_key_here
```

### 5. Run FastAPI backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

### 6. Run Streamlit frontend

Open another terminal inside `backend`:

```bash
streamlit run frontend.py
```

Frontend runs at:

```text
http://localhost:8501
```

## Example Use Cases

### Research Claim Analysis

Input:

```text
AI improves education
```

Output:

* Generated hypothesis
* Retrieved academic papers
* Evidence analysis
* Similar research papers
* Research chat over stored papers

### Dataset Analysis

Input CSV:

```csv
sleep_hours,exam_score
5,60
7,82
4,55
8,90
```

Output:

* Correlation score
* P-value
* Statistical significance
* Scatter plot
* Research report
* PDF download

## Resume Pitch

Digital Scientist is an AI-powered research assistant that combines LLM reasoning, academic paper retrieval, vector search, RAG-style research chat, statistical hypothesis testing, data visualization, and automated PDF report generation.

## Future Enhancements

* Cloud deployment
* User authentication
* Report history
* PDF paper upload
* Advanced embeddings
* Better citation ranking
* More statistical tests
* Research memory dashboard
