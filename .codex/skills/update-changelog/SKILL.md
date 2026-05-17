---
name: update-changelog
description: Update the root CHANGELOG.md before merges by grouping project changes under date headings, using Git history and current branch work. Use when the user asks to refresh, create, or maintain the changelog for this repository.
---

# Update Changelog

Maintain `/Users/diegovelez/Documents/PROJECTS/codex/yini-insurance-advisor/CHANGELOG.md` as a concise, date-grouped log of project changes.

## Workflow

1. Confirm the current branch and inspect `git status --short --branch`.
2. Read `CHANGELOG.md` if it exists.
3. Inspect commit history with `scripts/group_commits_by_date.sh`.
4. If the changelog does not exist, create it with `# Changelog` and one `## YYYY-MM-DD` heading per commit date.
5. Under each date heading, add short bullets describing the changes from commit subjects.
6. For uncommitted work, inspect the diff and add bullets under today’s date only if the user asked to include unreleased changes.
7. Keep entries factual and compact; do not invent work that is not visible in commits or diffs.

## Formatting Rules

- Keep the file at the project root as `CHANGELOG.md`.
- Use `## YYYY-MM-DD` headings.
- Use one flat bullet per change.
- Prefer concise action summaries over raw commit hashes.
- Merge related commits into one clearer bullet only when the underlying change is obviously the same unit of work.
- Preserve existing headings and append or update only what is needed.

## Default Policy

- Treat committed changes as the changelog source of truth.
- Do not include hashes in the changelog body unless the user explicitly asks.
- Do not add speculative release sections such as `Unreleased` unless the user asks.
- Before a merge, update the changelog for the branch being merged and confirm whether any uncommitted work was intentionally excluded.

## Commands

- Commit grouping: `./.codex/skills/update-changelog/scripts/group_commits_by_date.sh`
- Branch status: `git status --short --branch`
- Commit history: `git log --date=short --pretty=format:'%ad%x09%s' --reverse`
