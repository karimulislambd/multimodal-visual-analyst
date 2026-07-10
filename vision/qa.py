"""Free-form visual question answering over a single image."""
from __future__ import annotations

from vision import client
from vision.prompts import QA_SYSTEM


def answer(image_data_url: str, question: str, history: list[dict] | None = None) -> str:
    """Answer a question about the image, optionally with prior turns for context.

    History holds plain {role, text} turns; the image is re-attached to the latest
    question so the model always has it in view.
    """
    messages: list[dict] = [{"role": "system", "content": QA_SYSTEM}]
    for turn in history or []:
        messages.append({"role": turn["role"], "content": turn["text"]})
    messages.append(client.vision_message(question, image_data_url))
    return client.ask(messages)
