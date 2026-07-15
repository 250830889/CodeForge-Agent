"""Small, deterministic repository profile used by the CLI and prompt layer."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectProfile:
    root: Path
    languages: tuple[str, ...]
    manifest: str | None
    verification_commands: tuple[tuple[str, ...], ...]


def inspect_project(root: Path | None = None) -> ProjectProfile:
    root = (root or Path.cwd()).resolve()
    languages: list[str] = []
    commands: list[tuple[str, ...]] = []
    manifest: str | None = None

    if (root / "pyproject.toml").is_file():
        languages.append("Python")
        manifest = "pyproject.toml"
        commands.append(("python", "-m", "compileall", "-q", "."))
        if (root / "tests").is_dir():
            commands.insert(0, ("python", "-m", "unittest", "discover", "-s", "tests", "-v"))
    if (root / "package.json").is_file():
        languages.append("TypeScript/JavaScript")
        manifest = manifest or "package.json"
        try:
            package = json.loads((root / "package.json").read_text(encoding="utf-8"))
            scripts = package.get("scripts", {})
            if "test" in scripts:
                commands.append(("npm", "test", "--", "--runInBand"))
            if "lint" in scripts:
                commands.append(("npm", "run", "lint"))
        except (OSError, json.JSONDecodeError):
            pass

    return ProjectProfile(root, tuple(languages) or ("Unknown",), manifest, tuple(commands))


def render_profile(profile: ProjectProfile) -> str:
    commands = [" ".join(command) for command in profile.verification_commands]
    return "\n".join([
        f"Project root: {profile.root}",
        f"Languages: {', '.join(profile.languages)}",
        f"Manifest: {profile.manifest or 'not detected'}",
        "Verification: " + ("; ".join(commands) if commands else "no safe default detected"),
    ])
