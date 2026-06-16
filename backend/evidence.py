import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_evidence(hypothesis, papers):
    paper_text = ""

    for index, paper in enumerate(papers, start=1):
        paper_text += f"""
Paper {index}
Title: {paper['title']}
Published: {paper['published']}
Link: {paper['link']}
Summary: {paper['summary']}
"""

    prompt = f"""
You are a scientific research analyst.

Hypothesis:
{hypothesis}

Research papers:
{paper_text}

Analyze the evidence.

Return the answer in this format:

Supporting Evidence:
- point 1
- point 2

Opposing Evidence:
- point 1
- point 2

Research Gap:
- gap

Confidence Score:
Give a score from 0 to 100 and explain briefly.

Final Conclusion:
- conclusion
"""

    response = model.generate_content(prompt)

    return response.text