from fastapi import FastAPI

app = FastAPI(title="Mock Social Platform API")

@app.get("/health")
def health_check():
    return {"status": "healthy"}