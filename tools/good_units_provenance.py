"""Exact AI-side inputs consumed by the good-units evaluator.

The full source hash remains a historical audit fingerprint. Validation of the
live AI uses this shared extraction, so diagnostic/include edits do not pretend
to invalidate ratings, while changed doctrine flags still fail validation.
"""
import hashlib
import json
from pathlib import Path
import re

INPUT_SCHEMA = "priest-navy-affinities-v1"
INPUT_HASH_KEY = "AI RAW.per_affinities_sha256"


def parse_affinities(text: str) -> dict[str, dict[str, bool]]:
    blocks = re.split(r"(?=^#load-if-defined\s+)", text, flags=re.MULTILINE)
    by_host = {}
    for block in blocks:
        match = re.match(r"#load-if-defined\s+([^\s]+)", block)
        if not match:
            continue
        priest = re.search(r"\(set-goal\s+good-priests\s+(YES|NO)\)", block)
        navy = re.search(r"\(set-goal\s+good-navy\s+(YES|NO)\)", block)
        if priest and navy:
            by_host[match.group(1)] = {
                "good_priests": priest.group(1) == "YES",
                "good_navy": navy.group(1) == "YES",
            }
    return by_host


def load_affinities(path: Path) -> dict[str, dict[str, bool]]:
    return parse_affinities(path.read_text(encoding="utf-8-sig"))


def affinities_sha256(path: Path) -> str:
    payload = json.dumps(load_affinities(path), sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()
