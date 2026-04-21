<div align="center">

# Virtual Microscope

### An interactive, browser-based laboratory microscope simulator for medical and biology education

[![Live Site](https://img.shields.io/badge/live-virtual--microscope.online-00d4ff?style=for-the-badge)](https://virtual-microscope.online)
[![GitHub Pages](https://img.shields.io/badge/hosted%20on-GitHub%20Pages-181717?style=for-the-badge&logo=github)](https://github.com/ia7mad/Virtual-Microscope)
[![Bilingual](https://img.shields.io/badge/i18n-English%20%2F%20%D8%A7%D9%84%D8%B9%D8%B1%D8%A8%D9%8A%D8%A9-success?style=for-the-badge)](#internationalization)
[![No Build](https://img.shields.io/badge/dependencies-zero-brightgreen?style=for-the-badge)](#tech-stack)

**[Open the live demo &rarr;](https://virtual-microscope.online)**

<br>

<img src="preview.svg" alt="Virtual Microscope preview" width="640" />

</div>

---

## What it is

A faithful simulation of a clinical light microscope, optimised for teaching.

Hand a phone, tablet, or laptop to anyone — they immediately know what to do: a round eyepiece with a real specimen image inside, three objective lenses to switch between, coarse + fine focus dials, a lamp brightness knob, drag-to-pan, and a one-tap **Identify Structures** mode that labels what they're looking at.

The whole thing is **one HTML file with no build step**. Open it from a USB stick on the showcase laptop and it works.

## Highlights

| | |
|---|---|
| **Three objective lenses** | 10x Low Power · 40x High Power · 100x Oil Immersion, with a real "clunk" sound and turret-shadow sweep on every change. |
| **Dual-knob focus** | Outer coarse ring + inner fine knob, mirroring a real microscope, with synthesised dial-click sounds (no audio files). |
| **Lamp brightness** | Dial + slider (20 %–200 %), driving a real CSS filter on the slide. |
| **Identify Structures** | Tap once to overlay labelled markers for every structure on the current sample. |
| **Mini-map + scale bar** | Bottom-left mini-map shows the whole slide with viewport rectangle; bottom-right scale bar (100 µm / 25 µm / 10 µm) updates per lens. |
| **Bilingual UI** | Full English + Arabic with proper RTL layout. |
| **Mobile-tuned zoom** | A viewport-aware zoom factor (0.55x on screens ≤ 768 px) so 10x reads as a true low-power view on phones, not a punched-in 40x. |
| **Guided tour** | Scripted walkthrough of every control (desktop only — overlay would block the lens on small screens). |

## Specimen library

Eight specimens ship by default, each with English + Arabic name, description, and labelled markers:

`Normal Blood` · `Malaria Infection` · `Onion Root Cells (mitosis)` · `Gram-stained bacteria` · `Urine crystals` · `Histopathology section` · `Stool examination` · `Semen analysis`

Plus extra clinical cases: blood schistocytes, sickle cell, urine calcium oxalate, urine yeast.

Specimens are stored in **Supabase Storage** and fetched at load time, with the bundled [assets/](assets/) acting as fallback.

## Tech stack

- **Vanilla HTML / CSS / JavaScript** — no framework, no bundler.
- **Web Audio API** — synthesised dial-click and lens-change sounds.
- **Supabase** — live specimen list + admin curator panel.
- **GitHub Pages** — static hosting on `virtual-microscope.online` via the [CNAME](CNAME) file.

The whole runtime is a single ~5 700-line [index.html](index.html). Keeping it monolithic is deliberate: the showcase laptop must be able to open the file with zero dependencies.

## Quick start

```bash
git clone https://github.com/ia7mad/Virtual-Microscope.git
cd Virtual-Microscope
python -m http.server 8000
```

Open <http://localhost:8000>. That's the whole setup.

## File layout

```
Virtual-Microscope/
├── index.html        Main app (HTML + CSS + JS in one file)
├── admin.html        Curator panel for editing specimens
├── PROJECT.md        Full technical documentation
├── README.md         This file
├── CNAME             virtual-microscope.online
├── gen_qr.py         Generates the showcase QR-code SVG
├── preview.svg       Social-share preview (used as hero above)
├── qr-showcase.svg   QR code for the showcase poster
└── assets/           Specimen images (PNG)
    └── cases/        Extra clinical cases
```

## Documentation

For the deep dive — architecture diagram, every responsive regime, the iOS-Safari workarounds, the lens-change pipeline, and the Supabase schema — see **[PROJECT.md](PROJECT.md)**.

## Internationalization

The whole UI is bilingual (English + Arabic). Language is toggled via `body.lang-en` / `body.lang-ar` classes; CSS rules under each class flip text direction, font, alignment, and component spacing. Specimen content carries `{ en, ar }` objects.

## Credits

Created by **Ahmed · Hussin · Mohammed**.

[![WhatsApp](https://img.shields.io/badge/Contact-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)](https://wa.me/966550905017)
