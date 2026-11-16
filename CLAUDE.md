# Notes for Claude sessions in this repo

## Workplace Wellbeing Check (`wellbeing-check/`)

- After any commit that changes `wellbeing-check/` (or its synced copies `psychology-wiki/orgsvc.html`, `daneshsara/psy/orgsvc.html`), run the `wellbeing-tech-docs` agent (`.claude/agents/wellbeing-tech-docs.md`). If it records a business impact, run `wellbeing-business-plan` next.
- Both agents keep their state in `wellbeing-check/docs-agents/state.json` and edit two Persian Claude Docs documents (links in that file).
- Other sessions push to this repo too: always `git pull --rebase` before pushing.
