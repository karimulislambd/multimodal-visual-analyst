"""Thin wrapper around the Groq vision API: image encoding + message building.

Keeping the image/data-URL plumbing in one place means the QA and analysis
modules stay readable and easy to explain.
"""
from __future__ import annotations

import base64

from groq import Groq

import config


def encode_image(data: bytes, mime: str) -> str:
    """Turn raw image bytes into a data URL the model accepts."""
    b64 = base64.b64encode(data).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def mime_for(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower()
    return "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"


def client() -> Groq:
    return Groq(api_key=config.require_api_key())


def vision_message(text: str, image_data_url: str) -> dict:
    """Build a single user turn combining a text prompt and an image."""
    return {
        "role": "user",
        "content": [
            {"type": "text", "text": text},
            {"type": "image_url", "image_url": {"url": image_data_url}},
        ],
    }


def ask(
    messages: list[dict],
    *,
    temperature: float | None = None,
    json_mode: bool = False,
) -> str:
    """Send a chat request to the vision model and return its text reply."""
    kwargs: dict = {
        "model": config.VISION_MODEL,
        "messages": messages,
        "temperature": config.TEMPERATURE if temperature is None else temperature,
    }
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    resp = client().chat.completions.create(**kwargs)
    return resp.choices[0].message.content or ""
