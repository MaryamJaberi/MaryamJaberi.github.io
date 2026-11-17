# درنگ — Darang

Live: https://maryamjaberi.github.io/darang/

A single static page (`index.html`, no build, no server). It takes one short Persian
sentence (max 400 characters / 2 sentences), lists the separate stable readings of that
line with the ambiguity type of each, and — after the reader picks "منظورم این است" —
shows two rewrites that close that reading. Product spec: «درنگ — مشخصات محصول» v0.9.

## How it gets a model

Darang has no backend. The sentence goes straight from the visitor's browser to a model
provider the visitor chooses, with the visitor's own API key:

| Provider | Endpoint called | Auth header |
|---|---|---|
| Google Gemini (default) | `POST {base}/models/{model}:generateContent` | `x-goog-api-key` |
| Anthropic | `POST {base}/v1/messages` | `x-api-key` + `anthropic-dangerous-direct-browser-access: true` |
| OpenAI-compatible | `POST {base}/chat/completions` | `Authorization: Bearer` |

- The key is stored only in that browser's `localStorage`. It is never in this repo,
  never in a URL, never sent anywhere except the chosen provider. **Never commit a key.**
- "آزمایش اتصال" makes one tiny call and shows the provider's own error if it fails.
- "یک نمونهٔ آماده ببین" shows one pre-written example without calling any model.
- The same file also runs as a claude.ai artifact; there it uses the viewer's Claude
  account (`window.claude` sample capability) and hides the key settings.
- Default model names (`gemini-3.8-flash`, `claude-sonnet-5-5`) are editable in the page;
  update the `DEF` object in `index.html` when providers rename models.
- Gemini requests send no `temperature` (current Gemini models ignore or reject it).

## Test

Automated checks (jsdom, simulated providers) cover: request URL/headers/body for all
three providers, key never in the URL, fenced / prose-wrapped JSON, one retry on invalid
JSON, cache, local checks (not Persian, too long), 401/404/429 messages, threat caution,
the demo, and claude.ai mode. Not yet done: one live call with a real key in a real
browser, and the ten "golden sentences" of spec section 12.

## Known limits

- A provider must allow direct browser (CORS) requests.
- Output quality depends on the chosen model; the golden sentences are the acceptance test.
- Roadmap v2+ (context menu, side panel, comma chips, prior sentence) is not built.

© 2026 SoloNovate (Maryam Jaberi). All rights reserved.
