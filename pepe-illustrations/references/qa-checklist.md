# QA checklist

Run this on every picture before delivering it, whether Claude drew it or an image generator made it.

## Must pass

- 16:9 landscape (SVG viewBox `0 0 1600 900`).
- Clean white background.
- Pepe is there, on-model (small head, pear body, heavy lids, smirk), and reposed for the action.
- Pepe performs the core action, not decoration.
- A new metaphor for this material, not a copy of an old example.
- Strange, creative, interesting.
- Clean and sparse: the subject is no more than about 60% of the canvas; one calm empty area.
- One picture, one core structure.
- Labels are few, short, legible, and spelled correctly.
- Orange only for the main path or arrows.
- Red only for the key point, problem, warning or result.
- Blue only for side notes, feedback or system state.

## Detail floor (SVG route)

- `scripts/render.mjs` reports no warnings (≥ 150 shapes, palette only, 2-8 labels, fonts loaded).
- The main prop is built with construction parts and surface detail, ≥ 40 shapes.
- Containers show thickness; contents sit inside them, behind their front wall.
- Every paper, card, sign and screen has internal marks, varied.
- Pepe has effort or reaction marks if the action involves effort.
- At least 2 story details that reward a second look.
- At 2x zoom: no broken joins, pointy artefacts, objects poking through each other, or labels crossing lines.
- At least two render-review-fix rounds done, with weaknesses written down each round.

## Failure signs (redraw or fix)

- A title in the top-left ("Common pitfalls", "Workflow", "System architecture", "Roadmap").
- Pepe looks like a mascot, an emoji sticker or a cute cartoon, or has a different meme face.
- Pepe in the unchanged standing pose next to the action.
- Looks like a slide, a course page or a formal flowchart.
- Too many elements, arrows or nodes. Or the opposite: too few, crude, bare-box props.
- Text turning into explanatory paragraphs.
- Paper texture, shadows, gradients, beige, noise.
- Real UI screenshots or techy interfaces.
- Misspelled or unreadable labels.
- Stiff, with no absurd metaphor.
- Too similar to an example in `assets/examples/` or `assets/svg-examples/`.

## How to iterate

- **Too ordinary**: make Pepe the doer, and add a strange-but-logical metaphor.
- **Too busy**: cut nodes. Keep one action and 3-5 short labels. Don't strip the detail off what's left.
- **Too plain or crude**: add construction parts, contents with marks, story details. Check the detail floor.
- **Too cute**: deadpan, smug, serious. Strain shown by marks, not faces.
- **Too PPT**: remove titles, frames, neat grids and extra arrows. Turn it into a hand-drawn scene with perspective.
- **Too close to an example**: keep the meaning, change the main object and Pepe's action.
- **Wrong text**: fix the `<text>` (SVG) or edit locally (generated image). If a generated image has many errors, regenerate with fewer labels.

## Delivery test

A good picture makes the reader think "huh, that's odd" first, then get the structure within a second.

If the first impression is a tutorial page and not an absurd product sketch on white paper, it fails.
