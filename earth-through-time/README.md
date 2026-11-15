# Earth Through Time

Interactive teaching site: a world map and timeline from the origin of the universe to speculative futures (+10, +100, +1,000 years).

## Live site

- **GitHub Pages:** https://maryamjaberi.github.io/earth-through-time/
- **Repository:** https://github.com/MaryamJaberi/earth-through-time

If Pages is still building, open `index.html` on the `main` branch.

## What you can do

- Drag the timeline or use Previous / Next / Play
- Four layers per era: Earth and map, Life, Humans, Science of the age
- Future eras are labeled as projections, not forecasts

## Human-origins wiki (Persian) — `tabar/`

**ویکی تبار** is a Persian wiki of human origins built from podcast transcripts (Khodahafez Africa with Dr. Hamed Vahdati Nasab, Rokh podcast, asiatv) and Persian books and papers.

- Live: https://maryamjaberi.github.io/earth-through-time/tabar/
- 62 topic articles in six domains, 22 people, a library of books, papers, data, and 64 transcribed videos (`tabar/archive.html`)
- Tools: knowledge network and radial tree, coexistence of human species, migration map, Paleolithic sites (ROAD), radiocarbon map (p3k14c), ancient-DNA map (AADR v66.p1), domestication map, Earth clock, myth-or-fact quiz, and a gaps page listing what is still missing
- The atlas timeline now has seven human-story stops (7 mya to 10 kya) that link into the wiki, and supports deep links such as `index.html#era-neanderthal-world`

Data: p3k14c (Bird et al. 2022), AADR v66.p1 (Mallick et al. 2024, via the Poseidon archive), ROAD (ROCEEH, via roadDB), Natural Earth. Cite the original datasets when reusing them.

## Merged from two repositories (Nov 2026)

This repository is the single home of a project that used to live in two places:

- **`earth-through-time`** — the working, published site. It is what you see at the root of this repo.
- **`chrono-atlas`** — a React + Vite prototype of the same idea that was never built or published. Its source is kept under `prototype/` as a design reference, and its datasets were converted to JSON under `data/atlas/`.

Nothing from the live site was replaced. See `prototype/README.md` for what the prototype contributed and two caveats about it.

### `data/atlas/`

| file | contents |
|---|---|
| `atlasData.json` | paleogeography epochs, clades of life, mass extinctions, civilizations catalog, Iranian-plateau dynasties, Iran thematic panels, scholarly sources catalog |
| `thematicMapData.json` | historical boundary epochs, thematic entities, theme configs |

These are not yet wired into the live site; they are staged for it.

## Honest limits

This is not an archive of every national history or science book. It is a classified synthesis in American English from widely used reconstructions (ICS geologic time scale, paleogeography in the spirit of Scotese / Torsvik and Cocks, paleobiology, history of biology). Maps are schematic teaching drawings.
