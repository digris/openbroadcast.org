# Migration Progress

Analyze repository changes over a requested Git range and relate them to the migration roadmap.

Use this skill for requests such as:

- "show migration progress for the last 7 days"
- "show migration progress since Monday"
- "show migration progress from next to main"
- "show migration progress to main"
- "what migration work happened since <commit>"
- "compare recent work with the migration roadmap"

## Inputs

Interpret the user's request as a Git comparison range.

Examples:

- "last 7 days" → commits since 7 days ago through `HEAD`
- "since Monday" → commits since Monday through `HEAD`
- "to main" → compare the current branch with `main`
- "from next to main" → compare `next` and `main`
- explicit commit/tag/range → use the supplied Git revisions

If the intended range cannot be determined safely, ask for clarification rather than inventing a range.

## Sources

Use:

- Git commit history
- changed files and diff statistics
- relevant diffs when needed to understand what actually changed
- `docs/migration/README.md` as the migration roadmap

Do not infer migration progress from commit messages alone when the changed code can be inspected.

## Procedure

1. Read `docs/migration/README.md`.
2. Determine the requested Git range.
3. Inspect commits in the range.
4. Inspect changed files and relevant diffs.
5. Group changes by meaningful migration theme rather than listing every commit independently.
6. Compare those themes against the roadmap.
7. Distinguish clearly between:
   - roadmap items directly advanced,
   - migration-related work not yet represented in the roadmap,
   - unrelated work,
   - uncertain or incomplete work.
8. Report evidence using commit hashes and relevant file paths.
9. Do not modify files unless explicitly requested.

## Output

Prefer a concise report with these sections:

### Range

State exactly what Git range and dates were analyzed.

### Migration progress

Summarize meaningful migration work, grouped by theme.

For each theme include:

- what changed,
- relevant commits,
- important files,
- which roadmap goal it advances, if any.

### Roadmap status

Compare observed work with `docs/migration/README.md`.

Do not mark roadmap items complete merely because related work exists. Only describe completion when the repository evidence supports it.

### Other changes

Briefly mention significant changes in the range that are unrelated to migration.

### Gaps / next steps

Call out migration work visible in Git that is missing from the roadmap, unfinished work, or obvious next steps supported by the repository evidence.