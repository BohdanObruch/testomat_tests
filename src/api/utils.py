from __future__ import annotations

from typing import Any


def extract_first_id(payload: Any) -> str | None:
    if isinstance(payload, dict) and "data" in payload:
        payload = payload["data"]
    if isinstance(payload, list) and payload:
        first = payload[0]
        if isinstance(first, dict):
            return first.get("id") or first.get("key")
        return None
    if isinstance(payload, dict):
        return payload.get("id") or payload.get("key")
    return None
