# Design note: the portfolio as a living piece

Working document for whoever edits this site next (human or Claude).

## Brief
- Maryam wants the portfolio to update itself and to be a dynamic artwork, simple and clean.
- It is still a job-hunting site: recruiters must read the claims, open the work and download the CV within a minute. The art may never get in the way of that.

## What I looked at
- Self-updating developer portfolios that pull GitHub activity: useful mechanism, but the output is almost always a stats dashboard or a green contribution heatmap. Generic; not for this site.
- A London artist's portfolio whose hero is one living generative creature, with everything around it kept quiet. Lesson: one living thing, the rest disciplined.
- Amir B Ash, *Warp and Weft*: data drives a generative piece named after Iranian Termeh weaving.
- Carpetdiem (generative Azerbaijani carpets) and LIA's *Weaving*: the Jacquard loom is where weaving and computation first met. Punch cards were code.
- Persian carpet craft: designs are written as knot maps, a line of code per row, and every carpet carries two stories, the design's and the weaver's.

## From HubSpot's list of 23 graphic-design portfolios (taken, and left)
Taken, because they fit a product person's site and stay quiet:
- Sagmeister: project names that follow the cursor. Here: a label that follows the cursor over the loom's knots (and appears under the finger on a phone).
- Stefanie Brückler (small page-load detail) and Alex Trochut (animated signature): one opening moment. The feather mark in the nav draws itself, then the apps on the home screen switch on one by one, like a phone booting. Under a second and a half, once, skipped with reduced motion.
- Gleb Kuznetsov: a clear "available" indicator. Already there (the green dot in the hero); kept.
- "Keep it current" and "portfolios are never finished": the whole loom is this tip made literal.
- Peter Tarka and Tobias van Schneider: colour that belongs to each project. Every loom row uses its project's icon colours.

Left, on purpose:
- Custom cursors, collage homepages, "Enter" screens, multi-speed columns: they slow a recruiter down and would compete with the loom.
- Victor Work's choose-your-experience switch: the reduced-motion setting already gives people that choice without another control.
- Testimonials and client logos: good advice, but only with real quotes. Add them when Maryam has some.

## Concept: the loom (دار قالی)
Every change Maryam makes to one of her products is a knot. A loom for the year hangs on the page:
- rows = products (each in its own icon colour), columns = weeks of the loom year;
- woven weeks are a dark carpet field with knots sized by how much changed;
- weeks not yet lived are bare warp threads with a fringe, so the piece is literally unfinished and grows every week;
- a thin guard band frames only the woven part, so the border grows with the carpet.

It is honest (no invented numbers), personal (Persian craft, a weaver in Rotterdam), and it rewards coming back.

Hero (revised 15 Nov, after Maryam said the first pass still looked the same): the phone "home screen" became a garden carpet (chahar-bagh layout). An indigo border of saffron and pomegranate lozenges, corner pieces (lachak), a star medallion (toranj) holding her feather mark with two pendants, and the eight apps in a ring around it as the carpet's motifs, still clickable. The field is the sky over Rotterdam at the moment you visit (sun altitude computed in the browser); at night it is dark with stars. On load the carpet is woven from the bottom up, the way a weaver works, then the apps appear one by one. The loom further down is the same carpet's making-of.

Palette added for the carpet: indigo #2A2257, saffron #E8B04B, pomegranate #C2365A, wool #F4EEF9. The rest of the page keeps lilac paper and aubergine ink so the carpet is the one loud thing.

Third, the smallest: each project shows when it last changed.

## Kashi redesign (27 Nov 2026)
Maryam asked for a new layout and look, not another tweak. The lilac editorial page became a tiled wall:
- Palette from Persian tilework: glazed white #F2F5F7, lapis #1B2466 (hero and contact bands), lapis ink #131838, saffron #E8B04B, turquoise #17968F for "live", pomegranate #C2365A kept rare. The CSS variable names (--plum, --lilac) are unchanged so the case pages follow.
- One display face for both scripts: Markazi Text (Persian and Latin drawn together), over Hanken Grotesk / Vazirmatn for body. Young Serif is gone.
- Hero: headline across the full width of a lapis wall, then the carpet laid on its side (nine apps in an ellipse), hanging over the wall's lower edge onto the light page. Phones get the upright carpet. `rug_svg(..., wide=True)` draws the wide one.
- The carpet's lozenge border is reused once as a strip where lapis meets the page (hero bottom, contact top). Nowhere else.
- Selected work is four plates, two by two, so the whole set is visible before scrolling into any one of them. More projects is one row of four.
- Corners went from 22px to 6–10px: tile, not bubble.

## Rules
- Identity: glazed white, lapis, saffron; Markazi Text + Hanken Grotesk, Vazirmatn for Persian body. The carpet and its loom are the one bold element.
- No numbered eyebrows, no ALL CAPS, no stat counters, no heatmap squares. Knots are diamonds, like a knot seen from the back of a rug.
- Motion: one moment only. When the loom scrolls into view, the woven columns appear left to right like a shuttle passing; nothing loops. Respect reduced motion.
- Works in both directions: in Persian the loom weaves right to left.
- Everything degrades: no JavaScript or no data still leaves a readable page.

## Machine
- `.github/workflows/sync.yml` runs every six hours (and on demand). For each project repo whose HEAD changed, it builds the app and copies it to its folder on this site (`Dour/`, `Language-Learning-Party-Game/`, `earth-through-time/`, `ganjoor-no/`, `mafia/`). A failed build keeps the previous copy.
- `tools/pulse.py` reads the git history of every project and writes `assets/pulse.json` (commits per week, last change). It holds no timestamp of its own, so the site only gets a new commit when something really changed.
- `tools/build.py` regenerates the pages, then the workflow commits as github-actions and asks Pages to rebuild.
- Loom year starts on Monday 26 October 2026, the week the portfolio's history begins. On 25 October 2027 a second carpet starts.
