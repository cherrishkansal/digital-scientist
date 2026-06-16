import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_hypothesis(claim):
    prompt = f"""
Convert this claim into a formal scientific hypothesis.

Claim:
{claim}

Return only the hypothesis.
"""

    response = model.generate_content(prompt)
    return response.text