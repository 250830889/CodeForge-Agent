"""Safe local verification after an agent changes a repository."""

from __future__ import annotations

import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from .project_profile import ProjectProfile, inspect_project


@dataclass(frozen=True)
class CheckResult:
    command: tuple[str, ...]
    returncode: int
    duration_seconds: float
    output: str


def verify_project(root: Path | None = None, timeout_seconds: int = 120) -> tuple[ProjectProfile, list[CheckResult]]:
    profile = inspect_project(root)
    results: list[CheckResult] = []
    for command in profile.verification_commands:
        started = time.monotonic()
        try:
            completed = subprocess.run(
                command, cwd=profile.root, text=True, capture_output=True,
                timeout=timeout_seconds, check=False,
            )
            output = (completed.stdout + completed.stderr).strip()
            results.append(CheckResult(command, completed.returncode, time.monotonic() - started, output[-12000:]))
        except subprocess.TimeoutExpired:
            results.append(CheckResult(command, 124, time.monotonic() - started, "Verification timed out."))
        except OSError as exc:
            results.append(CheckResult(command, 127, time.monotonic() - started, str(exc)))
    return profile, results


def render_verification(results: list[CheckResult]) -> str:
    if not results:
        return "No verification command was detected for this repository."
    lines = []
    for result in results:
        status = "PASS" if result.returncode == 0 else "FAIL"
        lines.append(f"[{status}] {' '.join(result.command)} ({result.duration_seconds:.1f}s)")
        if result.returncode:
            lines.append(result.output or "No output captured.")
    return "\n".join(lines)
