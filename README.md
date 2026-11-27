# MaryamJaberi.github.io

Personal portfolio — Product Management & Product Design.

Live: https://maryamjaberi.github.io/

- `index.html`, `case/` — English portfolio; `fa/` — Persian portfolio (RTL)
- **Do not edit those HTML files by hand.** Edit the copy in `tools/build.py` and run `python3 tools/build.py`
- `assets/site.css` — shared design (Markazi Text + Hanken Grotesk; Vazirmatn for Persian body)
- `assets/icons.svg` — project icons (inlined into every page by the build)
- `assets/img/en`, `assets/img/fa` — screenshots, one set per language
- `cv.html` → `cv.pdf` — one-page CV (the PDF is printed from `cv.html`; regenerate it after editing)
- `assets/img/` — project screenshots, `assets/og.jpg` — link preview image
- `wellbeing-check/`, `psychology-wiki/` — projects hosted in this repo
- `mafia/` — static build of [MaryamJaberi/Mafia](https://github.com/MaryamJaberi/Mafia-new) (Miz Khoda / Mafia Host OS). Rebuild there with `npm run build:pages` and copy `dist-pages/` here as `mafia/`
- `Dour/`, `Language-Learning-Party-Game/`, `earth-through-time/`, `ganjoor-no/`, `mafia/` — hosted copies of the project repos (`*-new`). **Updated automatically**: `.github/workflows/sync.yml` runs `tools/sync.sh` every six hours (or on demand from the Actions tab), rebuilds any project whose repo changed, refreshes `assets/pulse.json` with `tools/pulse.py`, regenerates the pages and commits
- `assets/projects.json` — one record per product (names and descriptions in English and Persian, live URL, repo, status, last change). Written by `tools/build.py`; read it instead of scraping the pages
- `404.html` — written by `tools/build.py`. Forwards old addresses (renamed repos such as `/Mafia/` or `/Dour-new/`, wrong capitalisation) to the live folder; the list is `MOVED` in `tools/build.py`. **When a project folder is renamed, add the old name there**
- `tools/check_links.py` + `.github/workflows/links.yml` — every Monday the workflow opens every link on the portfolio and on the first page of each hosted project. A broken link opens one issue ("Broken links on the portfolio"); it closes itself when the links answer again. Run by hand: `python3 tools/check_links.py --local`
- The loom ("Every change is a knot"), the live Rotterdam sky and the "last change" lines come from `assets/pulse.json` and `assets/live.js`; the thinking behind them is in `tools/DESIGN.md`
- The source-guard script (`daneshsara/core/guard.js`) is kept off the portfolio pages and the CV on purpose; it stays on Daneshsara, Mafia and the wellbeing check
