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