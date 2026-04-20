# Virtual Microscope

An interactive, browser-based laboratory microscope simulator built for medical and biology education. Designed for the **Al Baha Health Cluster — National Laboratory Day** showcase, deployed at **[virtual-microscope.online](https://virtual-microscope.online)**.

The whole experience runs in a single HTML file with no build step: open it in any modern browser (desktop, tablet, or phone) and you have a working microscope.

---

## Table of contents

1. [What it is](#what-it-is)
2. [Live demo & repository](#live-demo--repository)
3. [Feature tour](#feature-tour)
4. [Specimen library](#specimen-library)
5. [Tech stack](#tech-stack)
6. [Architecture](#architecture)
7. [File layout](#file-layout)
8. [Running locally](#running-locally)
9. [Admin panel](#admin-panel)
10. [Deployment](#deployment)
11. [Internationalization](#internationalization)
12. [Accessibility & responsive design](#accessibility--responsive-design)
13. [Credits](#credits)

---

## What it is

A faithful simulation of a clinical light microscope, optimised for teaching. The student sees a round eyepiece with a real specimen image inside, can switch objective lenses (10x / 40x / 100x), turn coarse and fine focus dials, adjust the lamp brightness, pan the slide by dragging, and reveal labels for the structures they're looking at.

It is single-purpose by design: no logins, no progress tracking, no quizzes — just a microscope you can hand to anyone and they immediately know what to do.

## Live demo & repository

- **Production:** [https://virtual-microscope.online](https://virtual-microscope.online)
- **Repository:** [https://github.com/ia7mad/Virtual-Microscope](https://github.com/ia7mad/Virtual-Microscope)
- **Deployment:** GitHub Pages on the `master` branch, served from a custom domain via the [CNAME](CNAME) file.

## Feature tour

### The eyepiece
- Round, chromed eyepiece barrel with a rubber eyecup and a 3D drop shadow.
- The slide image lives inside an inner clip wrapper (`.eyepiece-clip`) that uses `clip-path: circle()` so the sample stays inside the round lens on iOS Safari (where `overflow:hidden + border-radius` fails for transformed children).
- Drag-to-pan with mouse, touch, or trackpad. Panning is clamped to the slide edges.

### Objective lenses
- Three buttons: **10x Low Power**, **40x High Power**, **100x Oil Immersion**.
- Switching plays a mechanical "clunk" sound, runs a turret-shadow sweep across the lens, smoothly scales the slide, and applies a transient blur + brightness drop to mimic the real moment of an objective swinging into place.
- On screens ≤ 768 px the magnifications are multiplied by **0.55** at runtime so 10x reads as a true low-power view rather than a punched-in 40x view (mobile eyepieces are about half the diameter of the desktop one).

### Focus
- Dual concentric dial: outer **coarse** ring, inner **fine** knob — the same arrangement as a real microscope.
- A linear focus slider mirrors the dial state for users who prefer dragging a bar.
- Each tick of either control plays a synthesised "click" through the Web Audio API (no audio files shipped).

### Lamp
- A lamp dial + brightness slider (20 %–200 %).
- Brightness is applied as a CSS filter on the sample image; the surrounding chromatic vignette also responds.
- Same dial-click sound as the focus knob.

### Identify Structures
- Toggle button overlays labelled markers on the visible structures of the current sample (e.g. *Malaria Parasite*, *Healthy red blood cell*).
- On mobile, the toggle becomes a pill button placed outside the lens so it never overlaps the eyepiece.

### Scale bar & mini-map
- A bottom-right scale bar updates with each lens (100 µm at 10x, 25 µm at 40x, 10 µm at 100x).
- A bottom-left mini-map shows the whole slide with the current viewport rectangle.

### Recenter Stage
- Snaps the slide back to the centre with a smooth animation.

### Guided tour (desktop only)
- A scripted tour highlights each control in sequence. Hidden on mobile and tablet (`pointer: coarse` or width ≤ 1024 px) because the tour overlay would block the lens on small screens.

### Bilingual UI (English / Arabic)
- Full RTL support via `body.lang-ar`.
- Every label, button, and case description is translated; the Arabic case-description font size matches English on mobile so layouts stay symmetric.

### Credit card
- A clickable card directly under the controls links to the team's WhatsApp ([+966 55 090 5017](https://wa.me/966550905017)).

## Specimen library

The default slide tray ships with the following cases, each with English + Arabic name, description, and labelled markers:

| ID | Specimen |
|---|---|
| `blood` | Normal Blood Sample |
| `malaria` | Malaria Infection |
| `mitosis` | Onion Root Cells (mitosis) |
| `bacteria` | Gram-stained bacteria |
| `urine` | Urine crystals |
| `histo` | Histopathology section |
| `stool_sample` | Stool examination |
| `semen_sample` | Semen analysis |

Plus extra clinical cases under [assets/cases/](assets/cases/): blood schistocytes, sickle cell, urine calcium oxalate, urine yeast.

Specimen images are stored in **Supabase Storage** (`microscope-media/specimens/...`) and fetched at load time. Local copies live in [assets/](assets/) as a fallback.

## Tech stack

- **Vanilla HTML / CSS / JavaScript** — no framework, no bundler, no transpiler.
- **Web Audio API** — synthesised dial click / lens clunk sounds (no audio assets).
- **Supabase JS client** (CDN) — fetches the live specimen list and the admin panel writes back to it.
- **GitHub Pages** — static hosting on a custom domain.
- **Python (one-off)** — [gen_qr.py](gen_qr.py) generates the showcase QR-code SVG.

The whole runtime is a single ~5 700-line [index.html](index.html). Keeping it monolithic is deliberate: the showcase laptop should be able to open the file from a USB stick with zero dependencies.

## Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│  index.html (single-page app)                                      │
│  ├── <style> ......... All CSS (responsive, RTL, animations)       │
│  ├── DOM             . Eyepiece, controls, slide tray, tour, HUD   │
│  └── <script>                                                      │
│      ├── Supabase client (live specimen list)                      │
│      ├── samples[] (fallback / default library)                    │
│      ├── State: currentMagnification, translateX/Y, focus, lamp    │
│      ├── Render loop: applyTransform() / clampPan() / updateMap()  │
│      ├── Lens-change pipeline: sound → turret sweep → scale → blur │
│      ├── Identify mode (markers + counter-scaled labels)           │
│      ├── Tour engine (desktop only)                                │
│      ├── Web Audio: _playDialSound / _triggerDialSound             │
│      └── i18n (lang-en / lang-ar toggle)                           │
└────────────────────────────────────────────────────────────────────┘

┌─────────────────────┐         ┌──────────────────────────────────┐
│  Supabase Storage   │ ◀─────  │  admin.html (curator tool)       │
│  microscope-media/  │ ──────▶ │  Add / edit specimens & markers  │
└─────────────────────┘         └──────────────────────────────────┘
```

Key implementation choices that show up across the file:

- **Inner clip wrappers** — `.eyepiece-clip` and `.turret-clip` exist solely to work around iOS Safari's failure to clip transformed children with `overflow: hidden + border-radius`. Both use `clip-path: circle()`, which Safari honours.
- **No transitions on `#slide-container` by default** — they are added via JS classes (`.zoom-anim`, `.recenter-anim`) only during the lens-change or recenter moments, so panning stays buttery.
- **`data-zoom`-driven lenses** — each `<button>` carries its own zoom factor, scale-bar text, and bar width, so adding a new objective is one line of HTML.
- **Mobile zoom factor** — `getZoomFactor()` returns `0.55` on screens ≤ 768 px and `1` otherwise; a single resize listener re-resolves magnification when the breakpoint flips (e.g. phone rotation).

## File layout

```
Virtual-Microscope-master/
├── index.html        Main app (~5 700 lines: HTML + CSS + JS)
├── admin.html        Curator panel for editing specimens (~1 500 lines)
├── CNAME             virtual-microscope.online
├── gen_qr.py         Generates the showcase QR-code SVG
├── preview.svg       Social-share preview
├── qr-showcase.svg   QR code for the showcase poster
└── assets/
    ├── blood_smear.png
    ├── gram_stain.png
    ├── histopathology.png
    ├── malaria_smear.png
    ├── onion_mitosis.png
    ├── polarized_crystals.png
    ├── semen.png
    ├── stool.png
    ├── urine_crystals.png
    └── cases/
        ├── blood_schistocytes.png
        ├── blood_sickle_cell.png
        ├── urine_calcium_oxalate.png
        └── urine_yeast.png
```

## Running locally

No build step. Either:

1. **Double-click [index.html](index.html)** — works for the UI, but Supabase fetches require `http(s)://`.
2. **Or serve over HTTP**, for example:
   ```bash
   python -m http.server 8000
   ```
   then open `http://localhost:8000/index.html`.

Specimens load from Supabase by default; if the network is offline, the bundled `samples[]` array in [index.html](index.html#L4176) keeps the app fully usable.

## Admin panel

[admin.html](admin.html) is a separate page for curating the live specimen list:

- Add a new specimen (name EN/AR, description EN/AR, image upload).
- Place markers by clicking on the image; each marker stores `{ top%, left%, label.en, label.ar }`.
- Edit or delete existing specimens.

Writes go directly to Supabase (`microscope-media` bucket + a `specimens` table). The anon key is embedded for read access; mutating actions require the policies to be set up server-side.

## Deployment

- Push to `master` on [github.com/ia7mad/Virtual-Microscope](https://github.com/ia7mad/Virtual-Microscope).
- GitHub Pages serves the repository root.
- The [CNAME](CNAME) file binds the site to `virtual-microscope.online`.

Deploy = `git push origin master`. There is no CI step.

## Internationalization

- The whole UI is bilingual (English + Arabic).
- Language is toggled via `body.lang-en` / `body.lang-ar` classes; CSS rules under each class flip text direction, font, alignment, and a few component-specific paddings.
- Specimen names, descriptions, and marker labels each carry `{ en, ar }` objects.

To add a third language, copy any `body.lang-ar` rule, change the suffix, add the matching keys in `samples[]` and the i18n strings block, and add a third button to the language switch.

## Accessibility & responsive design

The CSS contains six explicit viewport regimes:

| Regime | Approx. trigger |
|---|---|
| Desktop | width > 1366 px |
| Laptop | 1025–1366 px |
| Tablet portrait | 601–1024 px portrait |
| Tablet landscape | 601–1366 px landscape, height ≥ 600 px |
| Phone landscape | width ≤ 900 px, height ≤ 500 px |
| Phone portrait | width ≤ 600 px |

Each regime sizes the eyepiece, repositions the controls, and shows or hides peripheral chrome (the tour button is desktop-only, the Identify pill is the mobile alternative to the sidebar button, etc.).

Other accessibility details:
- All controls are real `<button>` / `<input>` elements with labels.
- The credit card uses an `aria-label` so screen readers announce "Contact creators on WhatsApp".
- `prefers-reduced-motion` queries dampen the lens-change animations.
- The `#sample-image` has descriptive `alt` text; markers have language-appropriate text.

## Credits

Created by **Ahmed · Hussin · Mohammed** for the Al Baha Health Cluster, National Laboratory Day 2026.

Contact the team: [WhatsApp +966 55 090 5017](https://wa.me/966550905017).
