# Repository Agent Guide

## Project conventions

* Use `uv` for Python dependency and environment workflows.
* Use `bun` for frontend package workflows.
* Prefer existing `Makefile`, `package.json`, and project scripts over ad-hoc commands.
* Follow existing repository patterns before introducing new abstractions or dependencies.
* Keep changes small, scoped, and reviewable.
* Keep it simple: inspect the relevant existing code and implement directly - no elaborate plans or agent orchestration unless there is a clear benefit.
* Do not expand the requested scope unless necessary to complete the task safely.
* Prefer adapting existing patterns over inventing replacement architecture.

## Safety

* Do not read, print, summarize, copy, or modify `.env`, `.envrc`, credential files, private keys, or deployment secrets unless explicitly requested for that exact file.
* Do not modify generated `dist/` output unless explicitly requested.
* Do not perform destructive or irreversible actions without explicit confirmation.

## Development stack

* The whole dev stack runs in docker compose: `make up`, `make logs`, `make ps`, `make down`.
* Single entry point: `http://obp-next.local:5000` (proxy -> `core`, `ui`, `pushy`).
* Code is bind-mounted: `runserver` and webpack reload on change. Celery does not - restart `core` after changing task code.
* Management commands run in the container: `make cli ARGS="<command>"`.
* Details: `devsupport/README.md`.

## Validation

* Run the smallest relevant validation first.
* Python: `make lint-be`, `make test-be-fast` / `make test-be` (host, `uv`).
* Frontend: `make lint-fe` (host, `bun`).
* Do not claim completion without fresh validation evidence; if validation cannot be run, state the gap clearly.

## Browser-assisted validation

* Use the `chrome-devtools` MCP (`.mcp.json`) against the local dev stack (`http://obp-next.local:5000`).
* Browser validation may include rendered output, user interactions, console errors, and network requests.
* Do not use browser automation against production or external authenticated systems unless explicitly requested.

## Repository structure

* `obp_core/` — core backend application code.
* `obp_ui/` — frontend/UI code.
* `config/` — project configuration.
* `services/` — service-related code.
* `devsupport/` — docker compose dev stack (see `devsupport/README.md`).
* `obp_core/legacy_apps/` - vendored and locally patched legacy dependencies that are unavailable or incompatible in their upstream versions.

## Git workflow

* Do not create commits, amend commits, rebase, merge, push, or otherwise modify Git history unless explicitly requested.
* Leave all implemented changes in the working tree for human review.
* `git status`, `git diff`, `git log`, `git show`, and other read-only Git commands are allowed.
* Never stage changes unless explicitly requested.
