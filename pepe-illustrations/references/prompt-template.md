# Fallback: image-generation prompts

**Only use this when the SVG route is blocked or the user explicitly asks for a generated image.** See "How pictures get made" in `SKILL.md`. Use whatever image tool the host provides (Canva `generate-image`, `image_gen`, etc.).

Generate each picture on its own. Never combine several pictures into one image.

If the tool accepts a reference image, attach `assets/pepe/pepe.png` so Pepe stays on-model.

```text
Generate one standalone 16:9 horizontal article illustration.

Visual DNA:
Pure white background. Minimalist black hand-drawn line art. Slightly wobbly pen lines. Lots of empty white space. Sparse red/orange/blue handwritten annotations. Clean absurd product-sketch feeling, but every drawn object is properly detailed: props have construction parts (straps, bolts, hinges, bricks, stitching), papers and cards carry small text lines and icons, containers show thickness. No gradients, no shadows, no paper texture, no complex background, no commercial vector style, no PPT infographic look, no cute mascot poster, no children's illustration, no realistic UI.

Recurring character required:
Pepe the frog, drawn in flat green (#7fa23a) with a thin dark outline: small head with two eye bumps on top, wide almond eyes with heavy half-closed lids and big black pupils, a wide thin brownish-orange smug smirk, tall pear-shaped body with a heavy belly, thin arms with long fingers, thick short legs with splayed frog toes. No clothes. Pepe must perform the core conceptual action, not decorate the scene. Deadpan, smug, serious, slightly bizarre, not cute. Pepe is the only coloured fill in the picture.

Theme:
{topic}

Structure type:
{Workflow / System close-up / Before-after / Character states / Concept metaphor / Layers / Route map / Mini comic}

Core idea:
{what this picture should say}

Composition:
{the exact scene: where Pepe is, what he's doing, the main object, how information flows}

Suggested elements:
{element 1} / {element 2} / {element 3} / {element 4}

Handwritten labels (in {language}):
{label 1} / {label 2} / {label 3} / {label 4} / {optional label 5}

Color use:
Black for line art. Orange for the main flow/path/arrows. Red only for key warnings/problems/results. Blue only for secondary notes or feedback/system state. Green only on Pepe.

Constraints:
One image explains only one core structure. Keep the main subject around 40%-60% of the canvas. Preserve at least 35% blank white space. Use at most 5-8 short handwritten labels. Do not write a title in the top-left corner. Do not write the structure type on the image. Do not make it a formal diagram, course slide, or dense explainer. Do not copy prior examples; invent a fresh visual metaphor for this specific material. Clear but not instructional, interesting but not childish, strange but clean, sparse but carefully detailed.
```

## Edit prompts

Remove a top-left title:

```text
Edit the provided image. Remove only the handwritten title "{text to remove}" and its underline from the top-left corner. Fill that area with the same clean white background, matching the surrounding blank paper. Preserve everything else exactly: characters, labels, paths, line style, composition, aspect ratio, and image quality. Do not add any new text or objects.
```

Make it stranger:

```text
Regenerate this illustration with the same core meaning and simple layout, but make Pepe more central to the conceptual action. Pepe should be doing the strange work that explains the idea, not standing beside the diagram. Keep it clean, sparse, hand-drawn, carefully detailed, and not cute.
```
