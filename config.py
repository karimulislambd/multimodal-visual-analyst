"""Central configuration for the multimodal visual analyst."""
from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

# Llama 4 Scout is multimodal (text + vision) and free on Groq.
VISION_MODEL: str = os.getenv("VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.2"))

# Guardrails for uploads (Groq caps base64 images at ~4 MB).
MAX_IMAGE_MB: int = 4
ALLOWED_TYPES: tuple[str, ...] = ("png", "jpg", "jpeg", "webp")


def require_api_key() -> str:
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Get a free key at https://console.groq.com "
            "and add it to a .env file (see .env.example)."
        )
    return GROQ_API_KEY
