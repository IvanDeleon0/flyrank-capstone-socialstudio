<div align="center">

  <h1>🧪 Mock Social Platform</h1>
  <p><b>A self-built fake social-media platform API for testing idempotent, rate-limit-aware, webhook-verified publishing — no real accounts, no real risk.</b></p>

  <img src="https://img.shields.io/badge/Status-Complete-brightgreen?style=flat-square" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.14-blue?style=flat-square&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.141-009688?style=flat-square&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Tests-Passing-brightgreen?style=flat-square" alt="Tests">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square" alt="License">

</div>

---

## 📖 About This Project

This is a hand-built replacement for a piece of infrastructure that was supposed to be provided but never shipped.

The original capstone brief (*Multi-Platform Social Campaign Publisher*) called for building against a **provided fake-platform server** at `starters/challenge-5-social/` — a sandbox that would mimic OAuth, rate limits, idempotency keys, and signed delivery webhooks, so no code would ever touch a real social account.

That starter folder was never built. When the capstone was later revised, students already partway through the original version were told to build the missing piece themselves. This repo is that piece.

Rather than reach for an off-the-shelf mock tool, I built it from scratch — a deliberate choice, since the graded behaviors (idempotency, rate-limit backoff, signed webhooks) are exactly the concepts worth understanding at the implementation level, not just configuring around.

### 🚀 What It Simulates

* **Fake OAuth token issuance** — a believable `/oauth/token` response, no real credential checking (this mock tests *my* publishing logic, not authentication).
* **Idempotent publishing** — the same `Idempotency-Key` sent twice returns the identical result instead of creating a duplicate post.
* **Rate limiting** — every 4th request to `/publish` returns `429 Too Many Requests` with a `Retry-After` header, simulating a real platform's throttling.
* **Signed webhook delivery** — after a successful publish, the server sends an HMAC-SHA256–signed callback to a webhook endpoint, so a receiving app can verify the notification is genuine.

---

## 🛠️ Built With

* **Language:** Python 3.14
* **Framework:** FastAPI + Uvicorn
* **Validation:** Pydantic
* **Testing:** Pytest + FastAPI's `TestClient`
* **Signing:** Python's built-in `hmac` / `hashlib` (HMAC-SHA256)
* **Outbound delivery:** `requests`

---

## 📥 Getting Started

### Prerequisites

* Python 3.10+ installed and on your PATH

### Installation

1. Clone the repo and move into this folder:
   ```bash
   git clone https://github.com/IvanDeleon0/flyrank-capstone-socialstudio.git
   cd flyrank-capstone-socialstudio/mock-social-platform
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1      # Windows PowerShell
   # source venv/bin/activate       # macOS/Linux
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn pydantic requests pytest httpx
   ```

4. Run the server:
   ```bash
   python -m uvicorn main:app --reload
   ```

   The API is now live at `http://127.0.0.1:8000`.

---

## 📡 Usage Guide

### `GET /health`
Basic liveness check.
```bash
curl.exe http://127.0.0.1:8000/health
```

### `POST /oauth/token`
Returns a fake bearer token.
```bash
curl.exe -X POST http://127.0.0.1:8000/oauth/token
```

### `POST /publish`
Publishes a post. Requires an `Idempotency-Key` header.

```bash
curl.exe -X POST http://127.0.0.1:8000/publish `
  -H "Content-Type: application/json" `
  -H "Idempotency-Key: unique-key-here" `
  -d '{"post_id":"post-1","platform":"instagram","caption":"hello","image_url":"https://example.com/img.png"}'
```

| Behavior | Result |
|---|---|
| Missing `Idempotency-Key` | `400 Bad Request` |
| Repeat request, same key | Same response as the original — no duplicate post |
| Every 4th request | `429 Too Many Requests` with `Retry-After: 5` |
| Successful publish | Result signed with HMAC-SHA256 and delivered to a webhook |

---

## 🧪 Running the Tests

```bash
pytest -v
```

Covers:
- ✅ Idempotent publish — duplicate `Idempotency-Key` → identical result
- ✅ Rate limiting — a `429` appears within 6 sequential requests

---

## 📂 Project Structure

```
📦 mock-social-platform
┣ 📜 main.py           # FastAPI app — all endpoints and logic
┣ 📜 test_main.py      # Pytest suite
┗ 📜 README.md         # You are here
```

---

## ⚠️ Known Limitations & Honest Notes

This mock is intentionally small — it exists to unblock the real capstone work, not to be a production-grade simulator. A few things worth knowing:

- **State is in-memory only.** The idempotency store and rate-limit counter are plain Python dicts/variables. Restarting the server wipes them. That's fine for a mock, but it's not how a real platform (or a production version of this) would work.
- **The rate-limit test is loose by design.** Because `publish_call_count` is global and shared across the whole test session, the test only asserts that *a* `429` shows up somewhere in 6 calls — not on a specific call number. A more robust design would reset or scope state per test.
- **Real detours hit while building this:**
  - Spent time chasing a `ModuleNotFoundError: No module named 'requests'` that turned out to be a **virtual environment mismatch** — `pip install requests` had been run in a different `.venv` than the one actually running the server. Fixed by explicitly checking `(Get-Command python).Source` to confirm which environment was active.
  - Accidentally created the first version of `main.py` *inside* the `venv/` folder instead of next to it — an easy mistake with VS Code's file explorer when a venv is freshly created.
  - Wrote a first draft of `test_main.py` with a whole test function accidentally duplicated via copy-paste, which also broke indentation (a second `def` nested inside the first instead of standing alone).

None of these were exotic bugs — they're the ordinary friction of a real development session, kept in here rather than smoothed over.

---

## 🗺️ Roadmap

- [x] Skeleton + health check
- [x] Fake OAuth token endpoint
- [x] Publish endpoint + idempotency
- [x] Rate limiting (`429` + `Retry-After`)
- [x] Signed webhook delivery
- [x] Tests + README
- [ ] *(Stretch, not required)* Persist idempotency/rate-limit state to a real store so it survives restarts

---

## 📜 License

MIT — this is a learning/portfolio project, free to reference or reuse.