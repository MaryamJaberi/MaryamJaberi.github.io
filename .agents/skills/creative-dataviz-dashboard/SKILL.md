---
name: creative-dataviz-dashboard
description: >-
  Design and build world-class, creative data visualizations and interactive dashboards.
  Synthesizes principles from 20 iconic visual platforms (The Pudding, Worldmapper,
  Earth Nullschool, Histography, Atlas of Economic Complexity, Gapminder, Information Is Beautiful,
  Musicmap, and Data Sketches) across 6 core pillars: Visual Hierarchy, Information Architecture,
  Interaction, Visual Encoding, Narrative, and Progressive Disclosure.
---

# Creative Data Visualization & Dashboard Design Skill

This skill teaches the principles, visual grammars, interaction paradigms, and implementation
patterns for crafting exceptional, narrative-rich data visualizations, interactive atlases,
and exploratory analytical dashboards.

--------------------------------------------------------------------------------

## 1. The 20 Inspiration Paradigms & Their Core Visual Mechanics

Category & Site | Visual Archetype | Key Mechanism | Best Applied To
:--- | :--- | :--- | :---
**1. Worldmapper** | Cartograms & Density Distortion | Geographic shapes scale by data metrics rather than landmass | Regional influence, dialect distribution, poet density
**2. The Pudding** | Scrollytelling & Editorial Walkthrough | Step-by-step visual dissection tied to scroll and narrative triggers | Historical debates, comparative poetic meters, stylistic evolution
**3. Earth Nullschool** | Vector Field & Streamline Particles | Smooth 60fps canvas particles showing current flows, forces, and temperatures | Poetic schools migration (Khorasan -> Iraq -> India), influence flow
**4. Atlas of Economic Complexity** | Bipartite Networks & Treemaps | Product spaces, trade balance node-link graphs, nested rectangular hierarchy | Vocabulary taxonomy, poetic forms, thematic interconnectivity
**5. The Museum of Maps** | Spatial Heritage & Layered Atlas | Curated historical overlays with deep zoom and chronological switches | Nasir Khusraw travelogues, Silk Road cultural exchange
**6. Histography** | Granular Timeline & Event Dot-Matrix | Millions of events represented as interactive dots that condense/expand across millennia | 1000+ years of Persian literature, poet lifespans and historical synchrony
**7. Atlas Obscura** | Curiosity-Driven Micro-Narratives | Geographic pinpoints with striking photography and story cards | Hidden gems, rare poetic devices, literary anecdotes and curiosities
**8. Europeana** | Multi-Faceted Cultural Archive | Faceted search with rich color palettes, timeline brackets, and media zoom | Complete manuscript archives, illuminated folios, audio-aligned recitations
**9. Musicmap** | Lineage Network & Genre Tree | Force-directed family tree with clickable expandable nodes and sub-branches | Shahnameh heroic genealogies, poetic metre evolution, radif lineages
**10. NASA Eyes & Exoplanets** | 3D Orbital Simulation & Scales | Interactive 3D spatial orbiters with scale comparison and temporal scrubbing | "Word Solar Systems" (central metaphor with orbiting satellite words)
**11. Global Forest Watch & Bird Migration** | Temporal Heatmaps & Animated Trajectories | Time sliders showing seasonal migratory paths across continents | Migration of poets to Mughal courts, pilgrimage routes, manuscript spread
**12. Our World in Data & Gapminder** | Motion Scatter Plots & Rosling Bubbles | Multi-dimensional 4D plots (X, Y, bubble size, color, time playback) | Historical century vs. lexicon diversity, sentiment vs. meter tempo
**13. World Inequality Database** | Distribution Curves & Percentile Deciles | Lorenz curves, cumulative area charts, clear inequality brackets | Zipf's law in Persian poetry, vocabulary frequency distribution
**14. Visual Capitalist & Information is Beautiful** | High-Impact Editorial Infographics | Bold contrast, bite-sized key metrics, visual metaphors, publication styling | Landing page highlight cards, summary statistics, striking metric callouts
**15. Visual Complexity & Data Sketches** | Hand-crafted Data Art & Chord Diagrams | Radial chord links, organic circular dendrograms, custom canvas visualizations | Tazmin/Esteghbal cross-poet dialogue, shared hemistich networks

--------------------------------------------------------------------------------

## 2. The 6 Foundational Pillars of Creative Visualization

### Pillar 1: Visual Hierarchy (سلسله‌مراتب بصری)
- **Primary Anchor**: Guide the user's eyes within the first 100 milliseconds to the dominant focal point (a bold hero stat, an active map marker, or a central node).
- **Scale Contrast**: Vary typography and element scale decisively (e.g. 48px key number vs. 13px label), never timid 2px differences.
- **Surface Elevation**: Use subtle layered depth (Z-index cards, translucent backdrops, delicate 1px borders with border-radius) rather than harsh drop shadows.
- **Breathing Room**: Preserve negative space around complex data nodes so patterns emerge clearly.

### Pillar 2: Information Architecture (معماری اطلاعات)
- **Mental Models**: Organize data according to how users think (e.g. Time & Space, Lineage & Ties, Language & Rhyme), not raw database schemas.
- **Card Sorting & Categorization**: Group disparate tools into coherent functional suites with clear visual tags.
- **Ubiquitous Cross-Linking**: Every data chip, poet tag, year, or metric must be a clickable portal to deeper exploration.

### Pillar 3: Dynamic Interaction & Micro-feedback (تعامل و بازخورد زنده)
- **Continuous Scrubbing**: Provide draggable timeline sliders or century dials with instantaneous UI reaction (<16ms response).
- **Brushing & Linking**: Hovering a node in one widget (e.g. a poet) highlights their position in the timeline, their points on the map, and their connections in the network simultaneously.
- **Contextual Tooltips**: Tooltips must feel like rich mini-cards, displaying exact values, contextual sparklines, and one-click actions.
- **Filter State Preservation**: Dynamic filtering must never cause jarring layout jumps; use smooth CSS transitions or FLIP animations.

### Pillar 4: Visual Encoding (رمزگذاری بصری دقیق)
Map data dimensions to human visual perceptions using Cleveland & McGill's hierarchy of graphical perception:
1. **Position along a common scale** (Best for quantitative comparison, e.g., timeline positions, bar lengths).
2. **Length / Area** (Good for relative scale; use circular bubbles where Area ∝ Value, radius = sqrt(val)).
3. **Color Hue** (Categorical grouping; maximum 6-8 distinct, accessible hues).
4. **Color Luminance / Saturation** (Sequential/diverging quantitative values, e.g., frequency heatmaps).
5. **Connection Lines & Curves** (Relational topology; bezier curves indicate flow/directionality).
6. **Motion & Streamline Velocity** (Particle speeds represent intensity or historical velocity).

### Pillar 5: Narrative & Scrollytelling (روایت‌گری داده‌محور)
- **Never dump raw numbers**: Contextualize every metric (e.g., instead of just "662 characters", say "662 characters spanning 3 mythical dynasties from Pishdadian to Sasanian").
- **Guided Discovery**: Offer curated starting points ("شاه‌بیت‌ها", "سفر ناصرخسرو", "مناظره حافظ و خواجو").
- **Scrollytelling Waypoints**: Lead the user on a guided path that pauses to highlight key historical anomalies or literary breakthroughs.

### Pillar 6: Progressive Disclosure (افشای تدریجی اطلاعات)
Follow Ben Shneiderman's golden rule of information visualization:
> **"Overview first, zoom and filter, then details-on-demand."**
1. **Overview (نگاه اجمالی)**: Clean summary card or high-level interactive map.
2. **Zoom & Filter (کاوش و پالایش)**: Filter by century, region, or meter.
3. **Details-on-Demand (جزئیات در زمان نیاز)**: Click to reveal full verse text, audio recitation, linguistic decomposition, and manuscript sources.

--------------------------------------------------------------------------------

## 3. UI Kit Design System for Creative Dashboards

### Color Palette (Persian Literature & Cultural Heritage)
```css
:root {
  --viz-primary: #0a6b60;        /* Persian Turquoise / فیروزه‌ای کهن */
  --viz-primary-light: #12877a;
  --viz-primary-soft: rgba(10, 107, 96, 0.08);
  --viz-gold: #c59b27;           /* زرین / تذهیب */
  --viz-gold-soft: rgba(197, 155, 39, 0.12);
  --viz-lapis: #1e3a8a;          /* لاجوردی */
  --viz-ruby: #be123c;           /* لعل و یاقوت */
  --viz-paper: #faf8f3;          /* کاغذ دست‌ساز کهن */
  --viz-ink: #1a202c;            /* مرکب مشکی */
  --viz-muted: #64748b;          /* خاکستری ملایم */
  --viz-border: #e8e2d4;         /* مرز خاکی ظریف */
}
```

### Component Patterns
1. **The Scrubber Timeline**:
   Horizontal year track with era bands, draggable thumb, and live poet chips that fade in/out based on lifespan overlap.
2. **The Flow / Chord Bridge**:
   Curved SVG bezier paths connecting source and destination nodes with directional gradient strokes.
3. **The Bubble Constellation**:
   Packed circles scaled by sqrt(frequency), with repulsion physics or flex-wrap sorting.
4. **The Metric Dossier**:
   Compact summary card with primary KPI, trend sparkline, and contextual comparison badge.

--------------------------------------------------------------------------------

## 4. Checklist for Evaluating Dashboard / Visualization Quality
- [ ] Is there an unmistakable primary focal point on page load?
- [ ] Can the user interact with the visualization within 3 seconds without reading instructions?
- [ ] Does dragging/filtering update the visual state instantaneously without layout shifts?
- [ ] Are complex numbers encoded with visual aids (proportional bars, color badges, sparklines)?
- [ ] Is the interface fully accessible, readable, and responsive on mobile and desktop?
- [ ] Does it tell a memorable story rather than acting as a static spreadsheet?
