# Pepe

Pepe is the recurring character in every picture. He replaces the original artist's black blob character ("小黑"). He isn't a mascot, a sticker or a cute decoration. He is a deadpan worker taking part in the system, doing something absurd but logical.

## Look

The canonical drawing is `assets/pepe/pepe.svg` (with `pepe.png` rendered next to it). Match it.

- Flat green body (`#7fa23a`), thin dark outline (`#1d2711`), darker green creases (`#3f5719`).
- **Small head** on a **tall pear-shaped body** with a heavy belly. The head is roughly a quarter of his height.
- Two eye bumps on top of the head. Wide almond eyes, big black pupils with small white highlights, **heavy half-closed upper lids**, brow creases and under-eye bags.
- **Smug smirk**: a wide, thin, brownish-orange (`#c26a3d`) mouth, with the right corner pulled higher and a small dimple.
- Thin-ish arms that hang to about hip height, with long splayed fingers.
- Thick short legs with splayed, pointed frog toes.
- Belly crease line and navel. Chest creases near the armpits.
- No clothes, no accessories, unless one prop is essential to the action (a hard hat for a "maintenance" scene is fine; a costume is not).

## Personality

- Takes the job completely seriously, even though the job is ridiculous.
- Calm, smug, a bit knowing. A low-key system operator.
- Dry humour, never mugging for the camera.
- A bit clumsy, never stupid.
- Looks like he is genuinely responsible for some part of the whiteboard sketch.

Expression stays the smirk with heavy lids by default. Strain shows through *marks* (sweat drops, strain ticks, motion lines) and pose, not a new face. If an idea really needs it, you may shift the pupils' direction or make the lids droopier; keep it subtle.

## Jobs he does

He does the core action of the metaphor:

- hauling material, pulling threads together from several sources
- stuck inside a breakpoint, or sitting on something to hold it shut
- working the "judgment" lever inside a machine
- standing in as a funnel or a filter, sorting things into bins
- slicing, pressing, weighing, stamping, stitching, patching
- holding the end of a path, opening a door, building a bridge plank by plank
- holding a warning sign at a pit
- reaching from a hole but failing to catch something

## Using the asset in a scene

`assets/pepe/pepe.svg` is built from named groups in a 300×480 coordinate space:

| Group | What | Notes |
|---|---|---|
| `#pepe-legs` | standing legs | redraw for sitting, walking, kneeling, kicking |
| `#pepe-body` | pear body, belly, creases | keep as is |
| `#pepe-arm-l`, `#pepe-arm-r` | hanging arms | redraw for every action |
| `#pepe-head` | head, eyes, lids, smirk | keep as is |

Anchors (in the 300×480 space): feet on the ground at y 462 (centred on x 150); bottom of body (for sitting) at y 388; shoulders at (98, 168) and (202, 168); head base at y 140.

To place him:

```xml
<g transform="translate(X Y) scale(S)" stroke="#1d2711" stroke-width="3.6">
  <!-- reposed legs -->
  <!-- #pepe-body contents -->
  <!-- reposed arms -->
  <!-- #pepe-head contents -->
</g>
```

- `S` is usually 0.5-0.75. Pepe should be a clear actor, not a speck: roughly 220-340 px tall standing in a 1600×900 scene.
- `X = targetX - 150*S` and `Y = targetY - 462*S` for feet at (targetX, targetY). For sitting, use `388*S` instead of `462*S`.
- Copy the `eyeL`/`eyeR` clipPaths into the scene's `<defs>` (they work inside the transformed group).
- After scaling down, thin creases vanish. Bump the 1.6-2 widths in the head and body to about 3 when S < 0.8.
- Draw order: legs → body → arms → head, so arms sit over the body and the head over the shoulders.

## Reposing arms and legs

Every scene needs a pose that does the action. Don't paste the standing pose.

**Arm**: a closed, filled path about 22-26 units wide, from the shoulder to the hand, ending in 3-4 long finger points. The top of the arm must be a *rounded* cap that tucks into the shoulder. A pointed top pokes up above the shoulder line and looks broken.
```xml
<!-- left arm reaching down to a lid at about (24, 420) -->
<path fill="#7fa23a" d="M98 168 C70 176 46 260 34 360 C32 380 30 396 26 410
  L10 418 L24 420 L14 430 L32 426 L30 438 L44 426 L50 434 L52 418
  C54 400 56 380 58 360 C64 290 80 226 100 200 C108 188 106 172 98 168 Z"/>
```
Mirror around x = 150 for the right arm. For pulling, bend the arm at an elbow with one extra curve. For carrying, bring both hands up in front of the belly. Hands gripping a rope or lever: draw the prop first, then the fingers curling over it.

**Sitting legs**: the thighs come forward as rounded lumps below the belly, knees over the edge, short shins hanging, splayed feet. See the worked example `assets/svg-examples/01-context-wont-close.svg`.

**Walking**: one leg straight under the body, the other angled back with the foot lifted and toes pointing down.

Render and look at a 2x crop of Pepe every time you repose him.

## Don't

- Don't make him a cute mascot, a children's cartoon, or an emoji sticker.
- Don't change his face into a different meme expression (crying, screaming, sad lips) unless the user asks.
- Don't give him complicated clothes, sparkly eyes or outfits.
- Don't let him stand in a corner watching.
- Don't let him steal the picture from the structure he's explaining.
- Don't draw him tiny, or in the unchanged standing pose.

## The test

If you remove Pepe and the core metaphor still completely works, he's decoration. Rewrite the scene so he is the one doing the action.
