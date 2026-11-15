# MaryamJaberi.github.io

Personal portfolio — Product Management & Product Design.

Live: https://maryamjaberi.github.io/

- `index.html`, `case/` — English portfolio; `fa/` — Persian portfolio (RTL)
- **Do not edit those HTML files by hand.** Edit the copy in `tools/build.py` and run `python3 tools/build.py`
- `assets/site.css` — shared design (Young Serif + Hanken Grotesk; Vazirmatn for Persian)
- `assets/icons.svg` — project icons (inlined into every page by the build)
- `assets/img/en`, `assets/img/fa` — screenshots, one set per language
- `cv.html` → `cv.pdf` — one-page CV (the PDF is printed from `cv.html`; regenerate it after editing)
- `assets/img/` — project screenshots, `assets/og.jpg` — link preview image
- `wellbeing-check/`, `psychology-wiki/` — projects hosted in this repo
- `mafia/` — static build of [MaryamJaberi/Mafia](https://github.com/MaryamJaberi/Mafia-new) (Miz Khoda / Mafia Host OS). Rebuild there with `npm run build:pages` and copy `dist-pages/` here as `mafia/`
- `Dour/`, `Language-Learning-Party-Game/`, `earth-through-time/`, `ganjoor-no/` — static copies of the project repos (`Dour-new`, `Language-Learning-Party-Game-new`, `earth-through-time-new`, `ganjoor-no-new`), served at their original URLs. To update one: build it in its repo (`npm run build` for the two games, `--legacy-peer-deps` for the language game) and copy `dist/` (or the plain files for the atlas and Ganjoor No) over the folder here
- The source-guard script (`daneshsara/core/guard.js`) is kept off the portfolio pages and the CV on purpose; it stays on Daneshsara, Mafia and the wellbeing check
