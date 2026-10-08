# Pepe, Imperial officer

Pepe is the recurring character in every picture. He replaces the original artist's black blob character ("小黑"). In this skill he is always **Pepe as an Imperial officer**: a frog in a black dress uniform and cape, hands clasped behind his back, looking sideways at whatever is going wrong.

He isn't a mascot, a sticker or a cute decoration. He is a deadpan functionary taking part in the system: supervising it, standing on it, inspecting it, signing off on it, or very obviously failing to fix it.

## The canonical asset

`assets/pepe/pepe-officer.svg` (with `pepe-officer.png` next to it) is an exact trace of the reference art. Transparent background, 1024×1536.

- Boot soles at y 1495, centred on x 590.
- Head centre about (585, 270).
- Hands are clasped behind the back.

**Use this file. Don't redraw him from memory.** Every scene where his standing pose works places the asset directly.

## Look (identity checklist)

When you check a scene, or have to draw him in another pose, all of these must be there:

- **Head**: Pepe's green frog head with darker green shading and a thick black outline. Eye bumps on top under the cap.
- **Eyes**: half-closed heavy lids, big black pupils with a small white highlight, looking sideways (to his left, the viewer's right).
- **Mouth**: the classic **frown**. Thick brownish-orange lips, downturned, the lower lip pushed out. Not a smile.
- **Cap**: black peaked officer's cap with a black visor, a silver button on the side, and a round white emblem (six-spoke hub inside a notched ring) on the front.
- **Tunic**: black, high stand-up collar, a diagonal front closure, a small rank plaque (four red squares over four blue) on the left chest, a small silver code cylinder either side of it.
- **Belt**: black, with a rectangular silver buckle that has a round button.
- **Trousers**: black, slightly flared (jodhpur cut) above the knee.
- **Boots**: tall, glossy black riding boots with grey highlight streaks.
- **Cape**: long black cape hanging from the shoulders behind him, down to the boots.
- **Pose**: standing three-quarter view, chest out, hands behind the back.

## Personality

- Takes the job completely seriously, even though the job is ridiculous.
- Stiff, self-important, quietly disappointed in everything.
- Dry humour, never mugging for the camera.
- Looks like he is officially in charge of some part of the whiteboard sketch.

The frown and side-eye are permanent. Reactions come from the scene around him (dents under his boots, sweat drops, a dropped clipboard), not from changing his face.

## Jobs he does

He does the core action of the metaphor. The standing pose suits a lot of them:

- **standing on** something to hold it shut, flat or down (a lid, a pile, a lever)
- **supervising** a machine, a conveyor or a queue from a platform
- **inspecting** a broken part, a pit or a leak, hands behind his back
- **guarding** a door or gate, blocking a path
- **presiding** over a sorting line or a scale
- **standing in** for the bottleneck itself: everything has to pass him

For actions that need hands (pulling, carrying, stamping, cutting), see "Other poses" below.

## Placing him in a scene

Copy `pepe-officer.svg` next to the scene SVG (for example into `assets/<slug>-illustrations/`) and reference it with an `<image>`:

```xml
<!-- outside the wobble group, so the trace stays crisp; after the props he stands on/in front of -->
<image href="pepe-officer.svg" x="X" y="Y" width="W" height="H"/>
```

- Keep the 2:3 aspect: `H = 1.5 * W`.
- Height in a 1600×900 scene: usually 280-380 px. He should be a clear actor, never a speck.
- To put his boots at (fx, fy): with `S = H / 1536`, use `X = fx - 590*S`, `Y = fy - 1495*S`.
- To flip him so he faces the other way: wrap the image in `<g transform="translate(2*fx 0) scale(-1 1)">` around his foot point. The emblem and plaque mirror too; that's acceptable at scene scale.
- Draw what's in front of him (a railing, a crate edge, papers in mid-air) after the `<image>`.
- `render.mjs` warns if a scene has no `pepe-officer` image, and if the file isn't found next to the scene.

## Other poses

When the action really needs his hands or a different stance, don't force the standing pose. Draw him in the scene's own line style (inside the wobble group), using `pepe-officer.png` as the visual reference, and tick every item on the identity checklist above.

- The colours are the asset's: tunic `#252629` with `#0a0b0d` outline, fabric highlights `#5b5c60` / `#6c6e71`, skin `#5a7b31` with shading `#374e20`, lips `#a4502b`, plaque `#f2322b` / `#2654c6`, silver `#979899` / `#e8e8ea`.
- Keep the cape, cap emblem, rank plaque and frown. Those four make him recognisable at a glance.
- Pose ideas: one arm forward holding a clipboard or stamp, the other still behind his back; both arms forward for carrying; leaning on a lever with one gloved hand.
- Render and compare a 2x crop of him against `pepe-officer.png` before delivering.

## Don't

- Don't redraw the standing pose; place the asset.
- Don't change his face (no smile, no crying, no screaming) unless the user asks.
- Don't drop the uniform, swap it for another outfit, or add props that compete with it.
- Don't make him tiny, or put him in a corner watching.
- Don't put the asset inside the wobble filter; it smears the trace.

## The test

If you remove Pepe and the core metaphor still completely works, he's decoration. Rewrite the scene so the action depends on him: his weight, his gate, his inspection, his signature.
