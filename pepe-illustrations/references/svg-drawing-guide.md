# SVG drawing guide

How Claude draws a scene by hand in SVG at the same level as the reference pictures. Read all of this before drawing. Open `assets/svg-examples/01-context-wont-close.svg` and its PNG to see every technique below in use.

## 1. Canvas skeleton

Every scene starts from this. Don't change the canvas size, filter or palette.

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" width="1600" height="900">
  <title>Short scene name</title>
  <defs>
    <style>@import url('https://fonts.googleapis.com/css2?family=Caveat:wght@600&amp;family=Ma+Shan+Zheng&amp;display=swap');</style>
    <!-- hand-drawn wobble for every line -->
    <filter id="wobble" x="-2%" y="-2%" width="104%" height="104%">
      <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="11" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
  <rect width="1600" height="900" fill="#fff"/>
  <g filter="url(#wobble)" stroke="#1a1a1a" stroke-width="2.6"
     stroke-linecap="round" stroke-linejoin="round" fill="none">
    <!-- ground, props (back to front), effort marks, annotations -->
  </g>
  <!-- Pepe: the traced asset, outside the wobble so it stays crisp -->
  <image href="pepe-officer.svg" x="X" y="Y" width="W" height="H"/>
  <!-- anything that must sit in front of Pepe goes here, in its own wobble group -->
</svg>
```

The `@import` only matters when the SVG is opened in a browser on its own. `scripts/render.mjs` loads the bundled fonts from `assets/fonts/` so rendering works offline.

## 2. The pen

| Use | Stroke | Width |
|---|---|---|
| Main outlines (props, containers, ground) | `#1a1a1a` | 2.4-2.8 |
| Interior detail (text lines on paper, stitching, bricks, ribs) | `#1a1a1a` | 1.2-1.6 |
| Accent strokes (handles, thick straps) | `#1a1a1a` | 5-7, with a white 2-3 stroke on top to make it a hollow tube |
| Annotation arrows | label colour | 2.2-3.2 |

- **Fills are white** (`#fff`) on every prop, so things in front cleanly cover things behind. The only colour fills are Pepe himself (his own palette) and small solid black dots (rivets, wheel hubs, ellipsis dots).
- No gradients, shadows, opacity tricks, patterns or textures. Depth comes from overlap, second faces and line weight.
- Dashed strokes (`stroke-dasharray="7 7"`) for stitching, seams, dotted motion trails, feedback loops.
- Everything goes inside the wobble group. Never draw outside it; straight vector lines give the game away.

## 3. Palette

| Ink | Hex | Only for |
|---|---|---|
| Black | `#1a1a1a` | all line art, primary labels, names of things |
| Orange | `#ef8a1f` | the main path or flow: arrows from A to B, the route |
| Red | `#e0302a` | the problem, warning, emotional point or result |
| Blue | `#2f6fd6` | secondary notes, system state, feedback loops, the "AI did this" note |
| Pepe | the asset's own colours (see `pepe-ip.md`) | Pepe only. The `<image>` isn't counted by the palette check |

Colour is scarce. Usually 1 orange path, 1 red note, 0-1 blue note. Blue is optional.

## 4. Composition

- Main subject takes about 40-60% of the canvas. At least 35% stays empty white, ideally one large calm area (often the top band).
- Keep everything within roughly x 120-1480 and y 140-820. Nothing touches the edges.
- One picture, one idea. Usually one big prop or scene on the left/centre, Pepe on or in it, and a small outcome on the right, linked by one orange path.
- Build a light 3/4 perspective for containers: draw the front face plus a top face and one side face (offset about +70 x, -50 y). Flat front-only boxes look like a diagram.
- **Layer order** (SVG paints in order): ground marks → back faces and interiors → contents → front faces → Pepe → effort marks → annotations. If contents should sit *inside* something, draw them between its back and its front face.

## 5. Detail floor (hard minimums)

A finished scene must meet all of these. `render.mjs` checks the shape count; you check the rest by eye.

- **≥ 150 drawn shapes** in the SVG. Finished scenes are usually 150-400.
- **The main prop alone has ≥ 40 shapes**: outline, second faces, construction parts (bolts, hinges, straps, buckles, handles, wheels, legs), surface detail (bricks, planks, stitching, ribs, seams).
- **Every container shows thickness** (an inner rim or a second face).
- **Every paper, card, screen or sign has internal marks**: 2-4 text lines, or an icon (image frame with a mountain, `< / >`, chart bars, a dot ellipsis, a check). Vary them; no two identical neighbours.
- **≥ 5 small contents items** when the idea involves "stuff" (information, tasks, messages): papers, bubbles, cards, at different rotations, overlapping naturally.
- **Pepe is placed so the action depends on him** (see `pepe-ip.md`), with **reaction marks** around him where it fits: the lid denting under his boots, strain ticks, sweat drops, a dust puff.
- **≥ 2 story details**: a tag, sticker, stray item on the floor, a dent, a mid-fall sheet with a dotted trail.
- **Ground cues**: a few short broken ground strokes under objects that stand on something. Never a full-width ground line.
- **2-8 handwritten labels**, each 1-4 words (2-8 Chinese characters). Plus any text that is part of a prop (a tag reading "200K") counts toward the 8.

### What "cheaping out" looks like (reject these)

- Rectangles with a word inside standing in for props.
- Arrows between boxes doing all the explaining.
- Blank papers, blank screens, empty containers.
- Pepe standing beside the action instead of being part of it.
- Perfectly symmetric, evenly spaced layouts.
- One render delivered without looking at it.
- Fewer, bigger shapes to "keep it minimal". Minimal means few *ideas* and lots of empty space. The things that are drawn are still drawn properly.

## 6. Techniques

**Paper / card with marks** (reuse as a `<g>` with translate + rotate):
```xml
<g transform="translate(486 560) rotate(-28)">
  <path fill="#fff" d="M0 0 L48 0 L62 14 L62 78 L0 78 Z"/>          <!-- sheet with folded corner -->
  <path d="M48 0 L48 14 L62 14" stroke-width="1.4"/>                <!-- the fold -->
  <path d="M9 22 L50 22 M9 34 L53 34 M9 46 L44 46 M9 58 L38 58" stroke-width="1.4"/>
</g>
```

**Hollow handle / strap** – thick dark stroke, then the same path in white on top:
```xml
<path d="M872 548 C860 560 860 616 872 628" stroke-width="7"/>
<path d="M872 548 C860 560 860 616 872 628" stroke-width="3" stroke="#fff"/>
```

**Hand-drawn arrow** – a curved shaft plus a separate open arrowhead (never `marker-end`):
```xml
<path d="M960 470 C1040 380 1180 380 1240 500" stroke="#ef8a1f" stroke-width="3.2"/>
<path d="M1222 486 L1241 504 L1248 478" stroke="#ef8a1f" stroke-width="3.2"/>
```

**Label** – no stroke, the bundled hand font:
```xml
<text x="150" y="530" font-size="48" fill="#e0302a" stroke="none"
      font-family="Caveat, 'Ma Shan Zheng', cursive" font-weight="600">won't close</text>
```
Size 44-54 for labels, 30-36 for text written on props. Point a label at its target with a short hand-drawn arrow in the same colour.

**Repetitive marks** – bricks, zipper teeth, stitches, grass, planks: generate the path data with a short loop (Python or JS), varying spacing and offsets a little so it doesn't look stamped. Write one `<path>` with many `M…L…` segments, or several shapes.

**Small solid dots** (rivets, hubs, ellipses): `<circle r="2.5-3.5" fill="#1a1a1a" stroke="none"/>`.

## 7. Render and review loop

```bash
node scripts/render.mjs path/to/01-scene.svg path/to/01-scene.png            # 2x PNG, 3200x1800
node scripts/render.mjs path/to/01-scene.svg /tmp/preview.png --scale 1      # quick 1600x900 look
```

It needs Playwright with a Chromium build (`npm i -D playwright`; set `CHROMIUM_PATH` to a browser binary if needed). It prints the shape count, labels, colours used, and warnings.

After every render:
1. Open the PNG and look at it whole. Does the idea land in one second? Is there a quiet empty area?
2. Look at a 2x crop of Pepe and the main prop. Check for broken joins, pointy artefacts, things poking through each other, labels colliding with lines, contents floating in front of a wall they should be behind.
3. Write down at least three concrete weaknesses ("tag hidden behind Pepe", "zipper teeth too sparse", "legs read as standing, not sitting").
4. Fix and re-render. At least two rounds before delivery.

## 8. Placing Pepe

See `pepe-ip.md`. In short: copy `assets/pepe/pepe-officer.svg` next to the scene, then add
`<image href="pepe-officer.svg" x="X" y="Y" width="W" height="1.5*W"/>` after the props he stands on or in front of, and outside the wobble group. For boots at (fx, fy) with height H: `S = H/1536`, `X = fx - 590*S`, `Y = fy - 1495*S`. Usually H is 280-380.

The worked example puts his boots on the suitcase lid at (600, 474) with H = 340, and adds a dent line and strain ticks under him.
