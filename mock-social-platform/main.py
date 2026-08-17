from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import secrets

app = FastAPI(title="Mock Social Platform API")

idempotency_store = {}
publish_call_count = 0

class PublishRequest(BaseModel):
    post_id: str
    platform: str
    caption: str
    image_url: str

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

@app.post("/publish")
def publish(request: PublishRequest, idempotency_key: str = Header(None)):
    global publish_call_count
    publish_call_count += 1
    if publish_call_count % 4 == 0:
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded",
            headers={"Retry-After": "5"}
        )

    if idempotency_key is None:
        raise HTTPException(status_code=400, detail="Idempotency-Key header is required")
    if idempotency_key in idempotency_store:
        return idempotency_store[idempotency_key]
    
    result = {
        "post_id": request.post_id,
        "platform": request.platform,
        "status": "published",
        "published_id": "fake-post-" + secrets.token_hex(6)
    }
    idempotency_store[idempotency_key] = result
    return result