# Documentation agents

Two agents keep the product documents current. Definitions: `.claude/agents/`.

| Agent | Keeps current | Runs |
| --- | --- | --- |
| `wellbeing-tech-docs` | Technical document: architecture, data model, privacy, future architecture, requirements forecast, ADRs, change log | after each change to `wellbeing-check/`, and on the daily scheduled run |
| `wellbeing-business-plan` | Business-plan document: six scenarios, recommended path, finance, legal and risk, hypotheses | when the tech agent records a business impact, when a price or decision changes, when pilot results arrive |

`state.json` holds the last reviewed commit, the document ids and the current business assumptions. The tech agent writes business impacts into `pending_business_impacts`; the business agent clears them.
