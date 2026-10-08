---
name: pepe-illustrations
description: Draw hand-sketched, slightly absurd 16:9 explainer illustrations starring Pepe the frog, for articles, posts, docs, and "how does this work" explanations. Use when the user asks for an illustration, explainer drawing, article image, shot list, or "a Pepe drawing of how X works", or asks to fix or iterate on one. Claude draws each picture itself as a detailed SVG and renders it to PNG. Image-generation tools (Canva, image_gen, etc.) are a fallback only.
---

# Pepe explainer illustrations

## What this is

Turn one key idea from an article or explanation (a judgment, a flow, a structure, a state, a metaphor) into a single 16:9 hand-drawn explainer picture: white paper, black pen lines, sparse red, orange and blue handwritten notes, lots of empty space, and **Pepe** doing the strange-but-logical work that makes the idea click.

Not a commercial illustration, not a PPT infographic, not a cute cartoon. It should look like a thoughtful product person sketched it on white paper to explain one thing.

Pepe must perform the core action. If you could delete Pepe and the metaphor still fully works, Pepe is decoration. Redesign the scene.

## How pictures get made

**Primary: Claude draws it.** Write the scene as SVG by hand, render it to PNG with `scripts/render.mjs`, look at the PNG, and revise. This is the default for every picture.

**Fallback: an image-generation tool** (Canva `generate-image`, `image_gen`, or whatever the host has). Use it only when:
- the user explicitly asks for a generated or painterly image, or
- the SVG route is blocked: there is no way to render (no Node, no Playwright/Chromium, and installing them fails), so you can't see what you drew.

Being slow, or the scene being hard to draw, is **not** a reason to fall back. When you do fall back, follow `references/prompt-template.md` and still run the QA checklist on the result.

## The bar: don't cheap out

The reference pictures in `assets/examples/` (the original artist's work, with a black blob character instead of Pepe) and the worked SVG in `assets/svg-examples/` set the level of detail. Every drawing has to reach it. In practice:

- **Props are built, not labelled.** A well has individual bricks and an inner wall. A suitcase has straps, buckles, stitching, wheels and a zipper with teeth. A machine has bolts, vents and a dial. A rectangle with a word in it is not a prop.
- **Contents have contents.** Every paper, card or screen inside the scene carries tiny marks: text lines, an icon, a code bracket, a little chart.
- **Pepe is reposed for the action.** Never paste the base standing pose unchanged. Redraw the arms and legs so he's actually pulling, pushing, sitting on or carrying the thing.
- **Story details.** At least one or two small touches that reward a second look: a luggage tag, a sticker, a stray sheet on the floor, sweat drops, strain marks.
- **Multiple passes.** Render, look, write down what's weak, fix it, then render again. Delivering the first render is never acceptable.

`references/svg-drawing-guide.md` has the full craft spec and hard numbers. `scripts/render.mjs` enforces a minimum shape count and the palette. Passing it is necessary, not sufficient.

## Read these as needed

Don't load everything at once:

- `references/svg-drawing-guide.md`: **always read before drawing.** Canvas, pen, fonts, layering, the detail floor, the render-and-review loop.
- `references/pepe-ip.md`: **always read before drawing.** Pepe's look, personality, how to place and repose the asset.
- `references/style-dna.md`: style, palette, text rules, hard noes.
- `references/composition-patterns.md`: structure types, how to invent a fresh metaphor, what not to copy.
- `references/qa-checklist.md`: checks before delivery and how to iterate.
- `references/prompt-template.md`: fallback image-generation prompts only.
- `assets/svg-examples/`: the worked SVG example. Read its source to see the expected level of detail and technique.
- `assets/examples/`: raster style calibration from the original artist. Look, don't copy.

## Workflow

### 1. Digest the source

Read the article, notes, link, or whatever the user wants explained. Pull out:
- the core point
- which paragraphs carry a turn in understanding
- which ideas would land better as a picture, and which are fine as text

Don't spread pictures evenly. Prioritize the cognitive anchors: a core judgment, two breakpoints, an input-output loop, a split, a before/after, one-source-many-uses, a handoff path, common traps, a change of state.

### 2. Shot list first (when planning)

If the user asks where pictures should go, or what to illustrate, give a shot list before drawing. For each picture:
- where it goes (after which paragraph)
- topic
- core meaning
- structure type
- what Pepe is doing
- key props
- suggested handwritten labels

Default 4-8 pictures for an article. 1-3 for a short piece. Rarely more than 9.

### 3. Draw each picture

When the user asks you to draw, generate, or make the pictures, don't stop to confirm. Draw each one as its own SVG; never put several pictures in one canvas.

For each picture:
1. Pick the metaphor and sketch the plan in your head: where Pepe is, what he's doing, the main prop, how information flows, the 3-6 labels.
2. Write the SVG following `references/svg-drawing-guide.md`.
3. Render: `node scripts/render.mjs <scene.svg> <scene.png>`.
4. Look at the PNG (and a 2x crop of the busiest area). Write down at least three specific weaknesses.
5. Fix them and re-render. Repeat until the QA checklist passes. Two rounds minimum.

Repetitive marks (bricks, zipper teeth, stitches, grass tufts) may be generated with a small script loop, but the composition, Pepe's pose and every prop's design are deliberate, hand-placed work.

Invent a new metaphor for each picture from the current material. Don't reuse the compositions from `assets/examples/` or `assets/svg-examples/` unless the user asks for that.

### 4. Check and iterate

Run through `references/qa-checklist.md`. Redraw or fix if:
- Pepe is decoration
- the picture is too full, or too empty and plain
- it looks like a flowchart or slide
- too much text, or misspelled labels
- a type title sits in the top-left ("Workflow", "Architecture", "Common pitfalls")
- it's cute, childish or stiff
- props are bare boxes, or papers are blank
- the background isn't clean white

### 5. Save and deliver

In a workspace, save to:

```text
assets/<article-slug>-illustrations/
  01-topic-name.svg
  01-topic-name.png
  02-topic-name.svg
  02-topic-name.png
```

Keep the SVG source next to each PNG so it can be edited later. Never overwrite existing assets unless the user asks.

Deliver the PNGs to the user (send the files where the host supports it). Then report:
- how many pictures, and what each one is for
- where they're saved
- which are strongest and which are optional

Keep it short. Let the pictures speak.

## Label language

Write the handwritten labels in the language of the source material. English text uses the bundled Caveat font. Chinese uses Ma Shan Zheng. Both are wired up in the SVG guide and the render script.
