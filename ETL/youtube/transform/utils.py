from __future__ import annotations

from json_repair import repair_json


def parse_json(text: str) -> dict:
    if text.strip() == "empty":
        return {}

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(f"No JSON object found in the text. {text}")

    json_str = text[start : end + 1]
    obj = repair_json(json_str, return_objects=True)
    if not isinstance(obj, dict):
        raise ValueError(f"JSON object is not a dictionary. {obj}")
    return obj
