"""Unit tests that run in CI without any API key.

They cover the deterministic plumbing: image encoding, MIME detection, and the
defensive JSON parser for structured analysis.
"""
from __future__ import annotations

from vision.analyze import _parse
from vision.client import encode_image, mime_for


def test_encode_image_is_data_url():
    url = encode_image(b"hello", "image/png")
    assert url.startswith("data:image/png;base64,")


def test_mime_for_jpeg_variants():
    assert mime_for("photo.jpg") == "image/jpeg"
    assert mime_for("photo.JPEG") == "image/jpeg"
    assert mime_for("shot.png") == "image/png"
    assert mime_for("art.webp") == "image/webp"


def test_parse_clean_json():
    raw = (
        '{"description":"a cat","objects":["cat"],"text_in_image":[],'
        '"colors":["black"],"key_insights":["it is sleeping"]}'
    )
    a = _parse(raw)
    assert a.description == "a cat"
    assert a.objects == ["cat"]
    assert a.colors == ["black"]
    assert a.key_insights == ["it is sleeping"]


def test_parse_json_with_surrounding_text():
    raw = 'Here is the result:\n{"description":"a dog","objects":["dog"]}\nHope that helps!'
    a = _parse(raw)
    assert a.description == "a dog"
    assert a.objects == ["dog"]


def test_parse_garbage_falls_back_gracefully():
    a = _parse("not json at all")
    assert a.description == "not json at all"
    assert a.objects == []
