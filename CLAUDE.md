@AGENTS.md

# Notes for Claude sessions in this repo

## Workplace Wellbeing Check (`wellbeing-check/`)

- After any commit that changes `wellbeing-check/` (or its synced copies `psychology-wiki/orgsvc.html`, `daneshsara/psy/orgsvc.html`), run the `wellbeing-tech-docs` agent (`.claude/agents/wellbeing-tech-docs.md`). If it records a business impact, run `wellbeing-business-plan` next.
- Both agents keep their state in `wellbeing-check/docs-agents/state.json` and edit two Persian Claude Docs documents (links in that file).
- Other sessions push to this repo too: always `git pull --rebase` before pushing.
- `nl-startup-expert` (`.claude/agents/nl-startup-expert.md`) keeps business-plan §8.4–8.5 (Dutch rules) current; re-verify after 1 Jan / 1 Jul or when a new service, hire, freelancer or country is added.
- `ip-protection-expert` (`.claude/agents/ip-protection-expert.md`) keeps §8.6 (IP) current. **Before pushing any new technical invention for `wellbeing-check/`, ask Maryam whether to file for protection first — publishing destroys patent novelty.**
