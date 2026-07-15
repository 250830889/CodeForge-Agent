# Architecture

The CLI starts by building a repository profile from local project files. The agent then uses permission-gated tools to inspect and edit the working tree. Every tool call is appended to a session audit log. After changes, `codeforge --verify` can execute deterministic local checks identified from the project profile.

The verification layer intentionally uses argument lists rather than shell strings, and caps each check with a timeout. This keeps project validation reproducible and limits command-injection risk in the verification path.
