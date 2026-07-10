"""One-click structured analysis: image -> clean JSON report.

This is the differentiator vs. a generic 'chat with an image' toy — it turns a
picture into structured, machine-readable data (Document/Visual Intelligence).
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from vision import client
from vision.prompts import ANALYZE_SYSTEM


@dataclass
class Analysis:
    description: str = ""
    objects: list[str] = field(default_factory=list)
    text_in_image: list[str] = field(default_factory=list)
    colors: list[str] = field(default_factory=list)
    key_insights: list[str] = field(default_factory=list)
    raw: str = ""  # kept for debugging / display fallback


def _coerce_list(value) -> list[str]:
    if isinstance(value, list):
        return [str(v) for v in value]
    if value:
        return [str(value)]
    return []


def _parse(raw: str) -> Analysis:
    """Parse the model's JSON defensively (handles stray fences/prose)."""
    match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
    if not match:
        return Analysis(description=raw.strip(), raw=raw)
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return Analysis(description=raw.strip(), raw=raw)
    return Analysis(
        description=str(data.get("description", "")),
        objects=_coerce_list(data.get("objects")),
        text_in_image=_coerce_list(data.get("text_in_image")),
        colors=_coerce_list(data.get("colors")),
        key_insights=_coerce_list(data.get("key_insights")),
        raw=raw,
    )


def analyze(image_data_url: str) -> Analysis:
    """Return a structured analysis of the image."""
    messages = [
        {"role": "system", "content": ANALYZE_SYSTEM},
        client.vision_message("Analyze this image and return the JSON.", image_data_url),
    ]
    raw = client.ask(messages, temperature=0.1, json_mode=True)
    return _parse(raw)
