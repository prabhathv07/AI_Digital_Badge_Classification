# AI-Assisted Digital Badge Classification System

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=flat&logo=spacy&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-351%20Passing-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-85%25+-brightgreen)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-2088FF?style=flat&logo=githubactions&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-100%25%2020%2F20-brightgreen)

> A rule-based, explainable web prototype that automates the classification of NJIT's digital badges according to the institution's locked taxonomy — achieving **100% accuracy on 20 real-world badges** and providing a full audit trail.

---

> ## NDA Notice
>
> This repository is a **portfolio showcase only**. I contributed to this project as an AI/ML Engineering Intern at NJIT's Learning & Development Initiative (2025–2026) and am bound by a **Non-Disclosure Agreement**.
>
> - This repo contains: architecture overview, my personal contributions, sanitized code patterns, metrics, and system design decisions
> - This repo does NOT contain: NJIT's full source code, confidential taxonomy rules, real badge data, or internal institutional documents
> - Full NDA details: [DISCLAIMER.md](./DISCLAIMER.md)
> - For contribution verification: vipparthi.prabhathvinay23@gmail.com
>
> ---

**Navigation:**
[What It Does](#what-it-does) · [The Problem](#the-problem) · [Architecture](#architecture) · [How It Works](#how-it-works) · [How to Use](#how-to-use) · [API Reference](#api-reference) · [My Contributions](#my-contributions) · [Results](#results) · [Code Samples](#code-samples-sanitized) · [Tech Stack](#tech-stack) · [Testing](#testing) · [Key Engineering Decisions](#key-engineering-decisions) · [What I'd Do Next](#what-id-do-next) · [ML/Data Science Addendum](#mldata-science-addendum)

---

## What It Does

Automates a previously manual, inconsistent process: classifying institutional digital badges into a 3-dimensional locked taxonomy (Category → Type → Level). Every classification decision is:

- **Deterministic** — no ML model ever makes a final classification decision; all logic is explicit rule chains
- **Explainable** — every output includes a structured plain-English explanation citing which signals triggered which rules
- **Auditable** — every classification and every reviewer override is permanently stored in a governance log
- **Human-controlled** — reviewers always have final authority and can override any stage

Built as a full-stack web application: FastAPI backend + React frontend + SQLite governance database.

---

## The Problem

NJIT issues digital badges across five institutional units — LDI, OSIL, Makerspace, NCE, and OGI. Each badge must be formally classified against a three-stage hierarchical taxonomy (Category → Type → Level) before it can be published. Prior to this system, classification was done manually — slow, inconsistent across reviewers, and with no structured audit trail.

The challenge: badge metadata arrives in three very different formats (structured JSON, a guided form, or plain free text), each requiring a different extraction strategy while producing the same standardized output.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        INPUT LAYER                          │
│         OBv3 JSON  ·  Proposal Form  ·  Free Text           │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    POST /ingest                             │
│                                                             │
│  Ingestion     → parse OBv3 JSON / map form fields /        │
│                  detect issuer from criteria URL domain     │
│  Normalization → convert any input to standardized          │
│                  Badge Fact Sheet (60+ structured fields)   │
│  Validation    → 30 validation checks (whitespace,          │
│                  duplicates, short content, series detect)  │
│                                                             │
│  OUTPUT: BadgeFactSheet object (60+ fields)                 │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    POST /classify                           │
│                                                             │
│  NLP Pipeline  → Layer 1: Phrase matching (130+ phrases)    │
│                  Layer 2: Regex patterns (44 rules)         │
│                  Layer 3: spaCy Bloom verb extraction       │
│                  Layer 4: LLM stub (disabled by default)    │
│                                                             │
│  Rule Engine   → Stage 1: Category (issuer + audience)      │
│                  Stage 2: Type (assessment + criteria)      │
│                  Stage 3: Level (cognitive depth)           │
│                                                             │
│  Explainability→ 8-element plain-English explanation        │
│  Governance    → Permanent audit log entry created          │
│                                                             │
│  OUTPUT: ClassificationResult with log_id                   │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    POST /review                             │
│                                                             │
│  Reviewer accepts or overrides any of the 3 stages         │
│  Override reason enforced (≥20 characters)                  │
│  Override type + level must be a valid taxonomy pair        │
│  Final decision permanently locked in governance log        │
└─────────────────────────────────────────────────────────────┘
```

**Key design principles:**
- No ML model ever makes a classification decision — all decisions are deterministic rule chains
- Missing signals trigger follow-up questions rather than blocking classification
- Every output is explainable with specific signal sources cited
- Every decision — original or overridden — is permanently auditable

---

## How It Works

### Step 1 — Ingestion & Normalization

The system accepts badge metadata in three formats and normalizes all of them into a single **Badge Fact Sheet** (60+ structured fields):

| Input Format | How It's Processed |
|---|---|
| **OBv3 JSON** | Parsed directly; issuer auto-detected from the `criteria.id` URL domain |
| **Proposal Form** | A 6-step plain-language guided form; a translation layer converts answers to Badge Fact Sheet fields |
| **Free Text** | Plain description runs through the full 4-layer NLP pipeline; follow-up questions appear for missing critical fields |

### Step 2 — NLP Signal Extraction (4 Layers)

| Layer | Method | What It Extracts |
|---|---|---|
| **1 — Phrase Dictionary** | Exact keyword matching against 130+ curated phrases | Audience type, achievement signals, skill/competency indicators |
| **2 — Regex Patterns** | 44 flexible regex rules | Paraphrased variants, assessment type signals, credential language |
| **3 — spaCy Bloom** | spaCy verb extraction mapped to Bloom's taxonomy | Cognitive depth level (remember → create) |
| **4 — LLM Stub** | Disabled by default; placeholder for future integration | Gap-filling for highly unstructured or ambiguous inputs |

Layers run in sequence. If Layer 1 resolves a signal with high confidence, later layers still run but their outputs are weighted. Missing signals after all 4 layers trigger structured follow-up questions — classification is **never blocked** by missing data.

### Step 3 — Deterministic Rule Engine (3 Stages)

All final classification decisions are made by explicit `if/elif` rule chains — not by any ML model.

**Stage 1 — Badge Category**
Determined by issuer identity + audience type. Each combination maps to exactly one category via a set of priority-ordered rules.

| Category | Determined By |
|---|---|
| Faculty & Staff Development | LDI issuer + NJIT employee audience |
| Continuing & Professional Education | LDI issuer + external professional audience |
| Co-Curricular / Extra-Curricular | OSIL issuer + student audience |
| Academic | Makerspace or NCE issuer + student audience |

**Stage 2 — Badge Type**
Determined by earning criteria + assessment method. Rules run in strict priority order — first match wins.

| Type | Key Signal | Assessment |
|---|---|---|
| Souvenir | Attendance only — no assessment required | None |
| Achievement | Auto-assessed or platform-tracked completion | Auto-assessed |
| Skill | Expert-scored demonstration of a specific skill | Expert-scored |
| Competency | Expert evaluation of KSAs in real-world context | Expert-scored |

**Stage 3 — Badge Level**
Level names are **type-specific** — they cannot be mixed across types.

| Type | Valid Levels (low → high) |
|---|---|
| Souvenir | Souvenir |
| Achievement | Foundational → Milestone → Terminal |
| Skill | Awareness → Application → Mastery |
| Competency | Demonstrated → Integrated → Exemplary |

### Step 4 — Explainability Output

Every classification produces an **8-element structured explanation** in plain English:
1. Category assigned + which issuer/audience signals triggered it
2. Type assigned + which assessment signals triggered it
3. Level assigned + which cognitive depth signals triggered it
4. Confidence level (High / Medium / Low)
5. All NLP signals used, each labeled with its source layer
6. Any signals that were missing and what follow-up was triggered
7. Complete list of rule IDs that fired *(internal IDs not disclosed — NDA)*
8. Reviewer action taken (accepted / overridden) and override reason if applicable

### Step 5 — Governance Log

Every classification — whether accepted or overridden — creates a **permanent, immutable governance log entry** containing:
- System recommendation vs. final human decision
- All signals used with source layer attribution
- Complete explanation text
- Override reason (if applicable) and exactly what changed
- Timestamp and reviewer ID

---

## How to Use

>  The full application is not publicly hosted (NDA). This section documents the user workflows to demonstrate the system's design and my understanding of the full product.

### User A — Badge Submitter

Navigate to the application and choose one of three input methods:

#### Option 1: Proposal Form
A 6-step guided form written in plain language — no taxonomy knowledge required. The submitter answers questions like "Who earns this badge?" and "How is it assessed?" A translation layer automatically converts answers to structured Badge Fact Sheet fields.

**After submission:**
1. Badge Fact Sheet is displayed with all extracted signals highlighted and their source layer labeled
2. Follow-up questions appear for any missing critical fields — these never block submission
3. Click **Submit for Review** → confirmation page shows submission status
4. Badge enters the reviewer's pending queue

#### Option 2: OBv3 JSON Paste
Paste any valid Open Badges v3 JSON object. The issuer is auto-detected from the `criteria.id` URL domain. Follow-up questions appear for any signals that could not be resolved automatically. Designed for badge issuers who already have structured badge data.

#### Option 3: Free Text
Describe the badge in plain everyday language. The NLP pipeline extracts signals automatically across all 4 layers. Plain-language follow-up questions prompt for any remaining missing fields. Designed for students or external parties evaluating badge equivalents from outside NJIT.

---

### User B — Reviewer

1. Click **Reviewer Login** in the navigation bar
2. Enter the reviewer access code (configured via environment variable)
3. View the **Pending Review** queue on the dashboard — each card shows badge title, issuer, and system confidence level
4. Click **View →** to open any pending badge
5. Review the full classification:
   - All extracted NLP signals with their source layer labeled (phrase / regex / spaCy / LLM)
   - Three-stage classification result with confidence level
   - Complete plain-English explanation
6. Choose an action:
   - **Accept** — confirms the system recommendation; locks in governance log
   - **Override** — change any stage; requires a mandatory written reason (≥20 characters); the override reason and what changed are permanently recorded

---

### Viewing the Governance Log

All classifications are permanently stored and accessible at `/logs`. Any user can view the full audit trail:
- System recommendation vs. final human decision side by side
- Override reason and exactly what changed
- Complete explanation text
- All signals used with source layer attribution
- Timestamps and reviewer identifiers

---

## API Reference

>  The API is part of the full NDA-protected codebase. JSON examples below use illustrative data — no real NJIT badge data is included.

### Endpoints Overview

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/ingest` | Convert any input format (form / OBv3 JSON / free text) to a Badge Fact Sheet |
| `POST` | `/classify` | Run the NLP pipeline + rule engine on a Badge Fact Sheet; creates governance log entry |
| `POST` | `/review` | Accept or override a classification; locks final decision in governance log |
| `GET` | `/logs` | Paginated list of all governance log entries |
| `GET` | `/logs/{id}` | Full detail for a single governance log entry |
| `GET` | `/health` | System status and spaCy model availability |
| `POST` | `/reviewer/auth` | Authenticate reviewer and receive access token |
| `GET` | `/reviewer/queue` | Pending queue, recent reviews, and reviewer stats |

---

### POST /ingest

Accepts badge metadata in any of three formats and returns a standardized Badge Fact Sheet.

**Request body:**
```json
{
  "input_type": "form",
  "payload": {
    "badge_title": "AI Literacy and Fundamentals",
    "badge_description": "Recognizes NJIT faculty who completed the AI Literacy course.",
    "issuer": "LDI",
    "audience_type": "njit_employee",
    "earning_criteria_text": "Complete all modules and pass the final assessment.",
    "assessment_required": "yes",
    "assessment_type": "final_assessment",
    "assessment_evaluator": "auto_assessed",
    "expert_evaluation_required": false
  }
}
```

`input_type` accepts: `"form"` | `"obv3_json"` | `"free_text"`

**Response:** Complete Badge Fact Sheet (60+ structured fields)

```json
{
  "badge_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "badge_title": "AI Literacy and Fundamentals",
  "issuer": "LDI",
  "audience_type": "njit_employee",
  "assessment_type": "final_assessment",
  "assessment_evaluator": "auto_assessed",
  "expert_evaluation_required": false,
  "follow_up_needed": false,
  "missing_signals": [],
  "normalized_at": "2026-04-28T10:00:00Z"
}
```

---

### POST /classify

Runs the 4-layer NLP pipeline and 3-stage rule engine on a Badge Fact Sheet. Creates a governance log entry and returns the full classification result.

**Request body:** The `BadgeFactSheet` object returned by `POST /ingest`

**Response:**
```json
{
  "badge_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "badge_title": "AI Literacy and Fundamentals",
  "issuer": "LDI",
  "classification": {
    "category": "Faculty & Staff Development",
    "type": "Achievement",
    "level": "Foundational",
    "confidence": "High"
  },
  "signals_used": {
    "issuer":           { "value": "LDI",                "source": "structured_field" },
    "audience_type":    { "value": "njit_employee",      "source": "structured_field" },
    "assessment_type":  { "value": "final_assessment",   "source": "structured_field" },
    "bloom_level":      { "value": "understanding",      "source": "spacy_verb" }
  },
  "explanation": "CATEGORY: Classified as 'Faculty & Staff Development' — issuer is LDI and audience is NJIT employee. TYPE: Classified as 'Achievement' — assessment is auto-assessed platform completion, no expert evaluation required. LEVEL: Classified as 'Foundational' — Bloom's verb extraction identified understanding-level cognitive depth.",
  "follow_up_needed": false,
  "missing_signals": [],
  "governance": {
    "log_id": "7e0b1234-...",
    "classified_at": "2026-04-28T10:00:00Z",
    "reviewer_status": "pending"
  }
}
```

---

### POST /review — Accept

```json
{
  "log_id": "7e0b1234-...",
  "reviewer_id": "reviewer_01",
  "reviewer_status": "accepted"
}
```

**Response:** Updated governance log entry with `reviewer_status: "accepted"` and timestamp.

---

### POST /review — Override

```json
{
  "log_id": "7e0b1234-...",
  "reviewer_id": "reviewer_01",
  "reviewer_status": "overridden",
  "override_reason": "Badge includes a reflection component requiring expert evaluation — should be Skill, not Achievement.",
  "override_category": "Faculty & Staff Development",
  "override_type": "Skill",
  "override_level": "Application"
}
```

**Validation rules enforced:**
- `override_reason` must be ≥ 20 characters
- `override_type` + `override_level` must be a valid taxonomy combination (e.g., `Skill` + `Foundational` is rejected — `Foundational` is only valid for `Achievement`)
- If all override values match the original recommendation, status silently resolves to `accepted`

---

### GET /logs

Returns a paginated list of all governance log entries.

```json
{
  "total": 47,
  "page": 1,
  "per_page": 20,
  "logs": [
    {
      "log_id": "7e0b1234-...",
      "badge_title": "AI Literacy and Fundamentals",
      "issuer": "LDI",
      "classification": { "category": "Faculty & Staff Development", "type": "Achievement", "level": "Foundational" },
      "reviewer_status": "accepted",
      "classified_at": "2026-04-28T10:00:00Z",
      "reviewed_at": "2026-04-28T11:15:00Z"
    }
  ]
}
```

---

### GET /health

```json
{
  "status": "ok",
  "version": "1.0.0",
  "nlp": {
    "spacy_available": true,
    "model": "en_core_web_sm"
  }
}
```

---

## My Contributions

| Area | What I Built |
|------|-------------|
| NLP Phrase Dictionary | 130+ student-friendly phrases for signal extraction across all taxonomy dimensions |
| Regex Pattern Rules | 44 regex rules handling paraphrased and variant language |
| Classification Engine | 3-stage deterministic rule engine (Category → Type → Level) |
| Validation Framework | Pytest suite — 351 tests (unit, integration, end-to-end), 100% pass rate |
| Synthetic Dataset | 20 synthetic badges covering all taxonomy branches and edge cases |
| ETL Pipeline | Excel → JSON → unified test set (29 master + 48 unified badges) |
| Governance Logging | Rule trace system for explainability and human reviewer overrides |

---

## Results

| Metric | Result |
|--------|--------|
| Classification accuracy (20 real badges) | **100%** across all 5 dimensions |
| Automated test suite | **351 tests — 100% pass rate** |
| NLP issuer detection (structured input) | 100% |
| NLP issuer detection (free text) | 100% |
| NLP audience detection (free text) | 80% |
| NLP assessment type detection (free text) | 60% |
| End-to-end scenario pass rate | 100% (7/7 scenarios) |
| Validation dataset | 29 master badges + 48 unified test badges |
| NLP-specific unit tests | 61 |

---

## Code Samples (Sanitized)

> These are sanitized excerpts demonstrating the architecture patterns I designed and built. Variable names, phrase content, and logic structure have been rewritten. No proprietary NJIT taxonomy rules or data are included.

### NLP Phrase Dictionary & Signal Extraction
```python
# Phrase dictionary — my design and curation (130+ phrases across all taxonomy dimensions)
STUDENT_PHRASES = {
    "achievement": ["completed", "finished", "passed", "earned", "mastered"],
    "skill":       ["demonstrate", "perform", "execute", "apply", "use"],
    "competency":  ["integrate", "analyze", "evaluate", "design", "create"],
}

def extract_signals(description: str) -> dict:
    """Extract classification signals from badge description text."""
    signals = {}
    for category, phrases in STUDENT_PHRASES.items():
        matches = [p for p in phrases if p in description.lower()]
        if matches:
            signals[category] = matches
    return signals
```

### 3-Stage Classification Engine
```python
def classify_badge(badge_metadata: dict) -> ClassificationResult:
    signals = extract_nlp_signals(badge_metadata)

    # Stage 1: Category — determined by issuer + audience signals
    category = classify_category(signals)

    # Stage 2: Type — determined by assessment method + evaluation signals
    badge_type = classify_type(signals, category)

    # Stage 3: Level — determined by cognitive depth via Bloom's taxonomy
    level = classify_level(signals, badge_type)

    return ClassificationResult(
        category=category,
        type=badge_type,
        level=level,
        confidence=signals.confidence_score,
        rule_trace=signals.matched_rules    # every decision is traceable
    )
```

### Validation Framework
```python
@pytest.mark.parametrize("badge,expected", load_test_suite())
def test_full_classification(badge, expected):
    result = classify_badge(badge)
    assert result.category   == expected.category
    assert result.type       == expected.type
    assert result.level      == expected.level
    assert result.confidence >= CONFIDENCE_THRESHOLD
```

---

## Tech Stack

| Category | Technology | Purpose |
|---|---|---|
| Backend | Python 3.11+, FastAPI | REST API, business logic |
| NLP | spaCy (en_core_web_sm) | Bloom's taxonomy verb extraction |
| NLP | Custom phrase dict + regex | Layers 1 & 2 signal extraction |
| ORM | SQLAlchemy 2.0+, SQLite | Governance log storage |
| Validation | Pydantic 2.0+ | Badge Fact Sheet schema enforcement |
| Frontend | React 18, Vite, Tailwind CSS | Submission + reviewer UI |
| HTTP Client | Axios | Frontend → backend API calls |
| Testing | pytest 7.x+, pytest-cov | 351-test validation suite with coverage reporting |
| Migrations | Alembic 1.13+ | SQLAlchemy schema migrations |
| Auth | python-jose, passlib | JWT-based reviewer authentication |
| CI/CD | GitHub Actions | Automated test + lint on every push |
| Containerization | Docker, Docker Compose | Reproducible dev and production environments |

---

## Testing

>  Full test suite is part of the NDA-protected codebase. Structure and coverage shown here for portfolio reference.

### Test Results
```
351 tests collected
351 passed, 0 failed
Pass rate: 100%
Runtime: ~3.8 seconds
```

### Coverage by Test Area

| Test Area | Scope | Tests |
|---|---|---|
| Accuracy matrix | 20 real NJIT badges — all 5 classification dimensions | 20 |
| End-to-end scenarios | 7 full workflows covering all 3 input types (form, OBv3 JSON, free text) | 52 |
| NLP extraction rate | Signal extraction accuracy measurement across structured and free-text inputs | 61 |
| Classification engine | Rule engine unit tests — one test per rule, all stages | 68 |
| Edge cases | 30 validation checks (whitespace, duplicates, short content, implied series) | 52 |
| Explainability | Explanation content completeness and plain-English quality | 33 |
| Governance logging | Log creation, override recording, immutability checks | 28 |
| API integration | Full round-trip API tests for all 8 endpoints | 37 |
| **Total** | | **351** |

### Running the Tests

```bash
# Full suite
pytest tests/ -v

# Specific area
pytest tests/test_accuracy_matrix.py -v
pytest tests/test_e2e_scenarios.py -v
pytest tests/test_nlp_extraction.py -v
```

---

## Run Instructions

>  Full source code is not publicly available (NDA). Setup instructions are shown here to demonstrate system architecture and deployment complexity.

**Option A — Docker (recommended)**
```bash
docker compose up --build
# → API:      http://localhost:8000
# → Swagger:  http://localhost:8000/docs
# → Frontend: http://localhost:5173
```

**Option B — Local**
```bash
# Set up Python environment
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Configure environment
cp .env.example .env
# Set: USE_LLM=false, DATABASE_URL, REVIEWER_PASSWORD, ALLOWED_ORIGINS

# Run database migrations
alembic upgrade head

# Start backend
uvicorn app.main:app --reload
# → API: http://localhost:8000
# → Swagger UI: http://localhost:8000/docs

# Start frontend (separate terminal)
cd frontend && npm install && npm run dev
# → http://localhost:5173

# (Optional) Load demo data
python scripts/load_sample_data.py

# Verify health
curl http://localhost:8000/health
# → {"status": "ok", "version": "1.0.0", "nlp": {"spacy_available": true}}
```

**Running tests with coverage**
```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

**Environment variables:**

| Variable | Default | Description |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./badges.db` | SQLAlchemy connection string |
| `USE_LLM` | `false` | Enable LLM gap-filling (requires API key) |
| `ANTHROPIC_API_KEY` | *(empty)* | Required only if `USE_LLM=true` |
| `REVIEWER_PASSWORD` | *(set in .env)* | Reviewer dashboard access code |
| `ALLOWED_ORIGINS` | `http://localhost:5173` | CORS allowed origins |

---

## Key Engineering Decisions

**Why deterministic rules over a ML model?**
Institutional taxonomy classification needs to be auditable. A neural model would achieve similar accuracy but couldn't explain *why* a badge was classified a particular way. Reviewers need to override decisions and trust the system — that requires full rule traceability. Every classification in this system cites the exact rules that fired.

**Why a 4-layer NLP pipeline?**
Single-method extraction (phrase matching alone) missed approximately 30% of signals in free-text badge descriptions. Layering phrase matching → regex → Bloom's verb extraction → LLM fallback gave full coverage across all input quality levels while keeping the primary path fast and explainable. Each layer handles what the previous one misses.

**Why human-in-the-loop override?**
No automated system should have final authority over institutional policy decisions. The override mechanism ensures reviewers remain in control. Requiring a minimum-length written reason (≥20 characters) for every override captures institutional knowledge — over time, override patterns reveal where the rule engine needs refinement.

**Why non-blocking missing signals?**
Early designs blocked classification when signals were missing. This created friction and slowed reviewer workflows. The redesign treats missing signals as follow-up questions rather than blockers — the system always produces a best-effort classification that reviewers can correct, rather than returning an error that stops the workflow entirely.

---

## What I'd Do Next

- **Full LLM integration** — Replace the LLM stub with a fine-tuned model (GPT-4o-mini or similar) to improve signal extraction from highly unstructured free-text inputs, particularly for badges from outside NJIT
- **Production hardening** — Migrate from SQLite to PostgreSQL, add proper authentication (JWT), deploy via Docker + Kubernetes, add rate limiting
- **Analytics dashboard** — Governance insights: classification drift over time, issuer trend analysis, override rate by category, reviewer disagreement patterns
- **LMS integration** — Connect to Canvas to auto-ingest course completion data as badge submission candidates
- **Active learning loop** — Feed reviewer override patterns back into the phrase dictionary and rule engine — high-override rules are candidates for refinement
- **Multi-tenant support** — Generalize the taxonomy configuration so other institutions can adopt the rule engine with their own taxonomies

---

## ML / Data Science Addendum

### Datasets

| Dataset | Source | Size | Preprocessing |
|---------|--------|------|--------------|
| Real NJIT badges | LDI, OSIL, Makerspace, NCE, OGI | 20 JSON payloads | Manual verification against taxonomy; used as accuracy matrix |
| Master badge inventory | Institutional badge records | 29 badge records | Standardized to CSV with skill category, learning outcome, delivery mode |
| Unified test set | Synthetic + master merged | 48 badges | Combined and validated for end-to-end testing |
| Synthetic core dataset | Generated from taxonomy rules | 20 badges (all branches) | Created to test every taxonomy path before real badge data arrived |
| NLP phrase dictionary | Student-friendly language patterns | 130+ phrases + 44 regex patterns | Manually curated; expanded iteratively from real badge description analysis |

### Model / Pipeline

The system deliberately uses **no ML model for final classification** — the rule engine is fully deterministic and explicit.

The NLP pipeline is a lightweight, layered rule-based extractor:

| Layer | Technique | What It Does |
|---|---|---|
| 1 | Phrase dictionary | Exact-match keyword spotting against 130+ curated phrases |
| 2 | Regex patterns | Pattern-based extraction covering paraphrased and variant language |
| 3 | spaCy Bloom | Verb lemmatization + mapping to Bloom's 6 cognitive levels |
| 4 | LLM stub | Placeholder — calls an LLM API for gap-filling when enabled |

All final decisions are made by explicit `if/elif` chains that mirror the locked institutional taxonomy. The NLP pipeline's job is only to extract signals — the rule engine decides.

### Full Metrics

| Metric | Result |
|--------|--------|
| Classification accuracy (20 real badges) | 100% across all dimensions |
| Unit test pass rate | 100% (351/351) |
| NLP issuer detection — structured input | 100% |
| NLP issuer detection — free text | 100% |
| NLP audience detection — free text | 80% |
| NLP assessment type detection — free text | 60% |
| End-to-end scenario pass rate | 100% (7/7) |
| Validation framework | 29 master + 48 unified + 61 NLP-specific tests |

> **Note:** The classification engine is deterministic. The NLP pipeline is used only for signal extraction — the rule engine reads those signals and applies the locked taxonomy rules to produce a classification decision.

---

## Disclaimer

This repository showcases my personal contributions to the AI-Assisted Digital Badge Classification project, a capstone built for NJIT's Learning & Development Initiative (Spring 2026).

| | |
|---|---|
| **NDA status** | I am bound by a Non-Disclosure Agreement with NJIT |
| **Source code** | Full source code remains property of NJIT — not included here |
| **Code samples** | All code in this repo is sanitized and rewritten for portfolio purposes |
| **Data** | No real NJIT badge data or confidential taxonomy rules are included |
| **Verification** | Contact me directly to verify my contributions |

See [DISCLAIMER.md](./DISCLAIMER.md) for full legal details.

---

## Contact

**Prabhath Vinay Vipparthi**

[LinkedIn](https://linkedin.com/in/prabhath-vinay-vipparthi-90544b225) · [Email](mailto:vipparthi.prabhathvinay23@gmail.com) · [GitHub](https://github.com/prabhathv07)
