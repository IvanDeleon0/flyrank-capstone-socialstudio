# Social Campaign Publisher — build agenda

A session-by-session plan, following the brief's phase structure (§8).
Each session ends with a concrete, testable result — the "gate" for that
phase — before moving to the next. This file tracks where we are; update
the checkboxes as sessions finish.

## How we'll work

- One step, one command at a time — same as before.
- Each session below is sized to be doable in a single sitting (roughly
  1.5-3 hours of focused work). Some phases need multiple sessions.
- We stop and rehearse the relevant probe (see brief §12) before checking
  a phase off, not just when the code "looks done."
- EVIDENCE.md gets a pasted proof (test output, curl transcript, log line)
  the moment a Definition-of-Done box is true — not saved for the end.
- BUILDLOG.md gets an honest entry any session AI writes non-trivial code,
  noting what it wrote, what was wrong, what changed.

---

## Phase 1 — Design (~4-6h)

- [ ] One-page design doc: problem statement, data model (campaigns,
      posts, statuses, tokens), API surface (routes + methods), layer
      sketch (HTTP → logic → data, adapter boundary), one explicit
      non-goal.
- [ ] `SocialPublisher` interface signature drafted (not implemented).
- [ ] Decide: FastAPI + which DB (Postgres via Docker, reusing the pattern
      from the revenue report project, or SQLite for simplicity).

**Gate:** design doc written and it's clear enough that Phase 2-4 have no
open questions about data shape or API surface.

## Phase 2 — Content generation (~8-12h)

- [ ] Fake platform server running locally (`starters/challenge-5-social/`
      — need to locate/set this up first).
- [ ] Image variant pipeline: Instagram 1080×1080, X 1600×900, subject
      inside safe zone.
- [ ] Caption composer: shared brand-voice fragment + platform-specific
      fragment, composed (not duplicated) per platform.
- [ ] Test asserting output image dimensions per platform.

**Gate:** running the pipeline on one sample post produces two correctly
sized images and two genuinely different captions.

## Phase 3 — Publishing system (~14-18h, the hard part)

- [ ] `SocialPublisher` interface implemented for real.
- [ ] `FakeInstagramPublisher` + `FakeXPublisher` adapters against the
      fake server.
- [ ] Idempotency key flow: same (post, platform) published twice, or
      retried after simulated timeout → exactly one post.
- [ ] Rate-limit handling: `429` + `Retry-After` respected, backoff, safe
      retry.
- [ ] OAuth tokens encrypted at rest (random IV), never logged.

**Gate:** Probe 1 (double-publish + retry-after-timeout → 1 post) and
Probe 2 (429 handling) both pass, demonstrated live, not just "should work."

## Phase 4 — Production reliability (~12-16h)

- [ ] Durable scheduler: post scheduled for a future time, worker picks
      it up and publishes.
- [ ] Crash recovery: kill the worker mid-batch, restart, confirm no
      duplicate publishes.
- [ ] Webhook endpoint (`POST /webhook/social-delivery`) verifies HMAC
      signature; forged/modified requests get `400`.
- [ ] Status only transitions on a verified webhook:
      `queued → publishing → published | failed`.
- [ ] Automated tests: image dimensions, duplicate-publish prevention,
      forged-webhook rejection, rate-limit behavior.
- [ ] README fully filled in (architecture diagram, real setup steps,
      honest limitations); EVIDENCE.md and BUILDLOG.md complete.

**Gate:** Probes 3-6 all pass (crash-resume, webhook forgery/validity,
image dimensions, no plaintext tokens).

## Phase 5 — Demo prep (~2-3h)

- [ ] Seed a demo campaign.
- [ ] Rehearse the full 6-minute demo flow (brief §13) twice, start to
      finish, including the deliberate failure moments (idempotency
      hammer, forged webhook, rate limit).
- [ ] Pick 2-3 lines of AI-assisted code you can explain in detail if an
      evaluator points at them.

**Gate:** demo run twice without you needing to check notes mid-flow.

---

## Session log

_(Add a line each session — date, what got done, what's next. Keeps
continuity between sessions without re-reading the whole chat history.)_

- 2026-08-14 — Repo created, `.gitignore` / `README.md` skeleton /
  `.env.example` committed and pushed. Ready to start Phase 1.
