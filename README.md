# AI-Assisted Digital Badge Classification System

> 🔒 Code is under NDA with NJIT's Learning & Development Initiative. This repo showcases architecture, contributions, and results only.

---

**Table of Contents**
[What It Does](#what-it-does) · [The Problem](#the-problem) · [Architecture](#architecture) · [Approach](#approach) · [My Contributions](#my-contributions) · [Results](#results) · [Code Pattern Examples](#code-pattern-examples-sanitized) · [Tech Stack](#tech-stack) · [Run Instructions](#run-instructions) · [Key Engineering Decisions](#key-engineering-decisions) · [What I'd Do Next](#what-id-do-next) · [ML/Data Science Addendum](#mldata-science-addendum) · [Disclaimer](#disclaimer) · [Contact](#contact)

---

## What It Does

Production NLP pipeline that classifies digital badges into a 3-dimensional institutional taxonomy — automatically, deterministically, and with full explainability. No black boxes. Every classification decision is traceable to a specific rule.

Built during an AI/ML Engineering internship at NJIT LDI (2025–2026).

---

## The Problem

NJIT issues hundreds of digital badges across departments. Manually categorizing each badge by **audience**, **type**, and **cognitive level** was slow, inconsistent, and didn't scale. The goal: automate classification while keeping every decision explainable to non-technical reviewers.

---

## Architecture

The system follows a deterministic pipeline with four main layers:

```
INPUT LAYER (OBv3 JSON · Proposal Form · Free Text)
       │
       ▼
POST /ingest
  - Ingestion → ingestion module
  - Normalization → normalization module
  - Validation → 30 validation error checks (whitespace, duplicates, implied series)
  OUTPUT: Badge Fact Sheet (60+ structured fields)
       │
       ▼
POST /classify
  - NLP Pipeline → Phrase matching, regex, spaCy Bloom, LLM stub
  - Rule Engine → Stage 1 (Category), Stage 2 (Type), Stage 3 (Level)
  - Explainability → 8‑element plain‑English output
  - Governance → Full audit entry
       │
       ▼
POST /review
  - Reviewer accepts or overrides any stage
  - Override reason enforced (≥20 chars, valid taxonomy pair)
  - Final decision locked in governance log
```

**Key principles:**
- Deterministic rule engine (no ML model ever makes a classification decision)
- Every output is explainable
- Every decision is auditable
- Human override is always supported

---

## Approach

### Ingestion & Normalization
Accepts OBv3 JSON, a guided proposal form, or free text. Resolves issuer via URL domain and maps everything to a Badge Fact Sheet (60+ fields).

### NLP Pipeline (4 layers)
- **Layer 1:** Phrase dictionary (130+ student‑friendly phrases)
- **Layer 2:** Regex pattern rules for flexible matching
- **Layer 3:** spaCy Bloom verb extraction (Bloom's taxonomy)
- **Layer 4:** LLM stub (disabled by default)

### Deterministic Rule Engine
- **Stage 1 (Category)** — based on issuer + audience (8 category classification rules)
- **Stage 2 (Type)** — assessment method + evaluation (11 type classification rules)
- **Stage 3 (Level)** — type‑specific levels (achievement: Foundational/Milestone/Terminal; skill: Awareness/Application/Mastery; competency: Demonstrated/Integrated/Exemplary)

### Explainability & Governance
Every classification generates a structured plain‑English explanation with rule IDs and signal sources, and a permanent audit log entry is created.

---

## My Contributions

| Area | What I Built |
|------|-------------|
| NLP Phrase Dictionary | 130+ phrase patterns for signal extraction across all taxonomy dimensions |
| Regex Pattern Rules | 44 regex rules handling paraphrased and variant language |
| Classification Engine | 3-stage deterministic rule engine (category → type → level) |
| Validation Framework | Pytest suite with 308 tests — unit, integration, and end-to-end |
| Synthetic Dataset | 20 synthetic test badges covering all taxonomy branches and edge cases |
| ETL Pipeline | Excel → JSON → unified test set (29 master + 48 unified badges) |
| Governance Logging | Rule trace system for explainability and human reviewer overrides |

---

## Results

| Metric | Result |
|--------|--------|
| Classification accuracy | 100% on 20 real NJIT badges |
| Test suite size | 308 tests |
| Test pass rate | 100% |
| NLP unit tests | 44 |
| End-to-end validation scenarios | 17 |
| Phrase patterns built | 130+ |
| Regex rules | 44 |
| Taxonomy dimensions classified | 3 (category, type, level) |

---

## Code Pattern Examples (Sanitized)

### Phrase Dictionary Structure
```python
# Signal extraction via phrase matching
SKILL_SIGNALS = {
    "demonstrate": ["demonstrate", "perform", "execute", "apply", "use"],
    "achievement": ["completed", "finished", "earned", "passed", "mastered"],
    "competency":  ["integrate", "analyze", "evaluate", "design", "create"]
}
```

### 3-Stage Classification Logic
```python
def classify_badge(badge_metadata: dict) -> ClassificationResult:
    signals = extract_nlp_signals(badge_metadata)

    # Stage 1: Determine category (audience + context)
    category = classify_category(signals)

    # Stage 2: Determine type (criteria + assessment signals)
    badge_type = classify_type(signals, category)

    # Stage 3: Determine level (cognitive depth via Bloom's)
    level = classify_level(signals, badge_type)

    return ClassificationResult(
        category=category,
        type=badge_type,
        level=level,
        confidence=signals.confidence_score,
        rule_trace=signals.matched_rules   # full explainability
    )
```

### Validation Framework Pattern
```python
@pytest.mark.parametrize("badge,expected", load_test_suite())
def test_full_classification(badge, expected):
    result = classify_badge(badge)
    assert result.category == expected.category
    assert result.type     == expected.type
    assert result.level    == expected.level
    assert result.confidence >= CONFIDENCE_THRESHOLD
```

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![spaCy](https://img.shields.io/badge/spaCy-09A3D5?style=flat&logo=spacy&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=flat&logo=pytest&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)

- **Language:** Python 3.11+
- **Backend:** FastAPI
- **NLP:** spaCy, regex, custom phrase matching, Bloom's Taxonomy mapping
- **Testing:** Pytest (308 tests)
- **Storage:** SQLite
- **Data:** JSON, CSV, Open Badge 2.0 format

---

## Run Instructions

Full source code not publicly available (NDA). Setup instructions available on request.

---

## Key Engineering Decisions

**Why deterministic rules over ML model?**
Institutional taxonomy classification needs to be auditable. A neural model would achieve similar accuracy but couldn't explain *why* a badge was classified a certain way. Reviewers need to override and trust the system — that requires full rule traceability.

**Why a 4-layer NLP pipeline?**
Single-method extraction missed ~30% of signals in free-text badge descriptions. Layering phrase matching → regex → Bloom's analysis → LLM fallback gave coverage across all input quality levels while keeping the primary path fast and explainable.

---

## What I'd Do Next

- Fine-tune a small transformer model on the curated labeled dataset to handle truly ambiguous cases
- Add active learning loop: human reviewer corrections feed back into phrase dictionary
- Build Streamlit dashboard for non-technical reviewers
- Expand to multi-institution badge taxonomy mapping

---

## ML/Data Science Addendum

### Dataset

| Dataset | Source | Size | Preprocessing |
|---------|--------|------|---------------|
| 20 real NJIT badges | LDI, OSIL, Makerspace, NCE, OGI | 20 JSON payloads | Manual verification against taxonomy; used as accuracy matrix |
| 29 master badges | Institutional badge inventory | 29 badge records | Standardized to CSV with skill category, learning outcome, delivery mode |
| 48 unified test set | Synthetic + master merged | 48 badges | Combined and validated for end‑to‑end testing |
| Synthetic core dataset | Generated from taxonomy rules | 20 badges (covering all branches) | Created to test every taxonomy path before real data arrived |
| NLP phrase dictionary | Student‑friendly language | 130+ phrases + 44 regex patterns | Manually curated; expanded iteratively from real badge descriptions |

### Model / Pipeline

The system deliberately uses no ML model for final classification (deterministic rule engine). The NLP pipeline is a lightweight, rule‑based extractor:

- **Layer 1 (Phrase dictionary)** — Exact‑match keyword spotting
- **Layer 2 (Regex)** — Pattern‑based extraction
- **Layer 3 (spaCy Bloom)** — Verb extraction and mapping to Bloom's taxonomy levels
- **Layer 4 (LLM stub)** — Placeholder for future generative extraction

All final decisions are made by explicit if/elif chains that mirror the locked institutional taxonomy.

### Metrics

| Metric | Result |
|--------|--------|
| Classification accuracy (20 real badges) | 100% (all dimensions) |
| Unit test pass rate | 100% (308/308) |
| NLP issuer detection (structured) | 100% |
| NLP issuer detection (free text) | 100% |
| NLP audience detection (free text) | 80% |
| End‑to‑end scenario pass rate | 100% (7/7) |
| Validation framework | 29 master badges, 48 unified test set, 61 NLP‑specific tests |

**Note:** The classification engine is deterministic (no ML model makes classification decisions). The NLP pipeline is used only for signal extraction; the rule engine reads those signals and applies locked taxonomy rules.

---

## Disclaimer

This repository showcases my personal contributions to the AI-Assisted Digital Badge Classification project completed for NJIT's Learning & Development Initiative.

- Full source code remains property of NJIT
- I am bound by a Non-Disclosure Agreement
- No confidential NJIT taxonomy rules, badge data, or internal documents are included
- Code snippets are sanitized excerpts demonstrating architecture and approach only

For verification of contributions, contact: vipparthi.prabhathvinay23@gmail.com

---

## Contact

**Prabhath Vinay Vipparthi**
[LinkedIn](https://linkedin.com/in/prabhath-vinay-vipparthi-90544b225) · [Email](mailto:vipparthi.prabhathvinay23@gmail.com) · [GitHub](https://github.com/prabhathv07)
