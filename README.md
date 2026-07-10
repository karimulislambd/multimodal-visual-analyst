# Multimodal Visual Analyst

[![CI](https://github.com/karimulislambd/multimodal-visual-analyst/actions/workflows/ci.yml/badge.svg)](https://github.com/karimulislambd/multimodal-visual-analyst/actions/workflows/ci.yml)
[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](#)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Lint: ruff](https://img.shields.io/badge/lint-ruff-000000?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)

> Upload any image and either **ask questions about it** in natural language or run a
> one-click **structured analysis** that turns the picture into clean, machine-readable JSON.

Powered by a **vision-language model** (Llama 4 Scout on Groq). Unlike a generic
"chat with an image" toy, this app also does **Visual Intelligence**: it extracts a
structured report — description, objects, on-image text, colors, and key insights — the
kind of output real document/image-understanding products are built on.

**Live demo:** _add your Streamlit URL here_

---

## What it does

| Mode | What you get |
|---|---|
| **Ask** | Free-form visual Q&A — grounded in what's actually visible, with follow-up context |
| **Structured analysis** | One click → JSON: `description`, `objects`, `text_in_image`, `colors`, `key_insights` |

## Why this project

| Skill it demonstrates | Where |
|---|---|
| **Multimodal AI / VLMs** | Vision message construction + inference (`vision/client.py`) |
| **Structured extraction** | JSON-mode analysis with defensive parsing (`vision/analyze.py`) |
| **Prompt engineering** | Separate, versioned prompts per mode (`vision/prompts.py`) |
| **Robust engineering** | Size guards, MIME handling, graceful JSON fallback |
| **MLOps** | Dockerfile, GitHub Actions CI, unit tests, minimal-toolbar deploy config |

## Architecture

```
                 ┌───────────────────────────────────────────┐
 image + text ─► │  Vision-Language Model (Llama 4 Scout)     │
                 │    ├─ Ask mode      → grounded visual Q&A  │
                 │    └─ Analyze mode  → strict JSON report   │
                 └───────────────────────────────────────────┘
```

## Tech stack

- **Model:** Groq `llama-4-scout` (multimodal) — free tier
- **UI:** Streamlit
- **Images:** Pillow (validation), base64 data URLs
- **Quality:** pytest · ruff · GitHub Actions · Docker

## Quickstart

```bash
git clone https://github.com/karimulislambd/multimodal-visual-analyst.git
cd multimodal-visual-analyst

python -m venv .venv
# Windows:  .venv\Scripts\activate
# macOS/Linux:  source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env        # then paste your free Groq key
streamlit run app.py
```

Get a **free** Groq API key at <https://console.groq.com>.

## Run the tests

```bash
pytest -q          # image encoding + JSON parsing, no API key needed
ruff check .
```

## How it works

1. **Encode** — the uploaded image is validated (type + size) and turned into a base64
   data URL the model accepts.
2. **Ask** — your question and the image are sent to the VLM with a system prompt that
   forces answers to stay grounded in what's visible.
3. **Analyze** — a JSON-mode request returns a structured report, parsed defensively so a
   stray fence or note never crashes the app.

## Roadmap

- [ ] Batch mode: analyze many images into one CSV/JSON table
- [ ] Domain presets (receipts, charts, ID cards) with tailored schemas
- [ ] Confidence self-check on each answer

---

Built by **Md Karimul Islam** — AI/ML Engineer · Computer Vision · LLM · XAI.
