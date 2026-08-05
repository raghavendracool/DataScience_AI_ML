"""
Module 11 — JSON Lines Experiment Logging
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def make_json_serializable(
    value: Any,
) -> Any:
    """Convert common values to JSON-safe structures."""
    if hasattr(value, "item"):
        return value.item()

    if isinstance(value, dict):
        return {
            str(key): make_json_serializable(
                item
            )
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple)):
        return [
            make_json_serializable(item)
            for item in value
        ]

    return value


def append_jsonl(
    path: str | Path,
    record: dict[str, Any],
) -> None:
    """Append one experiment record as one JSON line."""
    destination = Path(path)
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    safe_record = make_json_serializable(
        record
    )

    with destination.open(
        "a",
        encoding="utf-8",
    ) as file:
        file.write(
            json.dumps(
                safe_record,
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
        )
