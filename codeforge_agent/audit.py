"""Append-only, local audit records for agent execution."""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any


class AuditLogger:
    """Stores one JSON record per line so a task run can be inspected later."""

    def __init__(self, session_id: str, root: Path | None = None) -> None:
        self.session_id = session_id
        base = root or Path.home() / ".codeforge" / "audit"
        base.mkdir(parents=True, exist_ok=True)
        self.path = base / f"{session_id}.jsonl"

    def record(self, event: str, **data: Any) -> None:
        payload = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "event": event, **data}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, default=str) + "\n")
