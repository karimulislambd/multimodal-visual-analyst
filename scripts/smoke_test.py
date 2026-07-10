"""End-to-end smoke test against the live Groq vision API.

Generates a simple image, runs both modes (Q&A + structured analysis), and
prints the results. Run:  python scripts/smoke_test.py
"""
from __future__ import annotations

import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image, ImageDraw  # noqa: E402

from vision import client  # noqa: E402
from vision.analyze import analyze  # noqa: E402
from vision.qa import answer  # noqa: E402


def _make_image() -> str:
    img = Image.new("RGB", (320, 180), "white")
    d = ImageDraw.Draw(img)
    d.rectangle([20, 30, 140, 150], fill="royalblue")
    d.ellipse([170, 40, 270, 140], fill="orange")
    d.text((30, 155), "INVOICE 2026", fill="black")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return client.encode_image(buf.getvalue(), "image/png")


def main() -> None:
    url = _make_image()

    print("[Q&A] Q: What shapes and text are in the image?")
    reply = answer(url, "What shapes and text are in the image? Be brief.")
    print("[Q&A] A:", reply, "\n")

    print("[Analyze] running structured analysis…")
    a = analyze(url)
    print("  description :", a.description)
    print("  objects     :", a.objects)
    print("  text        :", a.text_in_image)
    print("  colors      :", a.colors)
    print("  insights    :", a.key_insights)

    ok = bool(reply) and bool(a.description)
    print("\n" + ("PASS - vision pipeline is live" if ok else "CHECK - review output above"))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
