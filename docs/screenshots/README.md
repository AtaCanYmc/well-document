# Visual Asset & Screenshot Guidelines

Visual documentation should convey architectural clarity and command results faster than plain prose. Follow these guidelines to maintain design integrity across all visual elements.

---

## Technical Standards

1. **Format Hierarchy**:
   - Vector Graphics: **SVG** (mandatory for banners, architecture diagrams, and sequence flows).
   - High-Density Captures: **PNG** (retina 2x, 1200px max width for terminal sessions and UI components).
   - Animations / Demos: **WebM** or optimized **GIF** (< 3 MB).

2. **Styling & Color Palettes**:
   - Dark background preferred (`#0f172a` or `#1e293b`).
   - Accent colors must maintain WCAG AA contrast against backgrounds.
   - Avoid low-contrast pastels or generic AI gradient slop.

3. **Compression & Hygiene**:
   - Compress all PNG images with `oxipng` or `pngquant` prior to committing.
   - SVGs must have metadata and unnecessary editor tags stripped via `svgo`.
   - Never commit raw uncompressed desktop screenshots.

---

## Directory Inventory

| Asset | Type | Purpose | Dimensions |
| --- | --- | --- | --- |
| `banner.svg` | SVG | Primary README banner | 1200 × 320 px |
| `terminal-audit.png` | PNG | Terminal demonstration of audit scorecard | 1200 × 700 px |
| `archetypes-flow.svg` | SVG | Visual architecture flow | 800 × 400 px |
