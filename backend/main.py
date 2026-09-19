from fastapi import FastAPI

app = FastAPI(title="KOHLER Unified Enterprise AI Agent")

@app.get("/")
def root():
    return {"message": "KOHLER AI Agent is running"}