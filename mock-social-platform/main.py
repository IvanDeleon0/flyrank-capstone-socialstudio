from fastapi import FastAPI
import secrets

app = FastAPI(title="Mock Social Platform API")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/oauth/token")
def issue_token():
    return {
        "access_token": "fake-token-" + secrets.token_hex(8),
        "token_type": "bearer",
        "expires_in": 3600
    }