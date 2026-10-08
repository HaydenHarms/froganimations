# Character trace loop

How `pepe-illustrations/assets/pepe/pepe-officer.svg` was made from `reference.png`, and how to redo it if the character art changes.

## Pipeline

1. **Colour-layer trace** (`trace.py`): upscale the reference 3x, cluster its opaque pixels into 18 colours (Lab k-means), clean the label map (median filter, then merge every speck under 90 px into the colour around it), and trace each colour layer with potrace. Layers are stacked largest-first on a silhouette base, so there are no gaps.
2. **Hand-built insignia** (`fit2.py`): the geometric parts that tracing turns to mush (cap emblem, rank plaque, code cylinders, hat and buckle buttons) are built as parametric vector shapes. Each is fitted to the reference by Nelder-Mead on a blurred pixel difference, with bounded parameters so nothing can collapse. Each sits on a patch in the surrounding fabric colour that hides the traced original. The cap emblem's placement is locked to values measured on a 9x grid, because the blurred metric drifts on the cap's shading.
3. **Score** (`score.mjs` + `diff.py`): render the SVG on white and compare it with the reference composited on white. Prints the mean absolute error and the share of pixels off by more than 40. `crops.py` and `grid.py` make zoomed side-by-side checks.

## Rerun

```bash
pip install opencv-python-headless potracer cairosvg scipy
python3 -c "import cv2; im=cv2.imread('reference.png', -1); a=im[...,3:]/255; cv2.imwrite('ref_on_white.png', (im[...,:3]*a + 255*(1-a)).astype('uint8'))"
python3 trace.py reference.png base.svg 18 10 1.0 0.2 1 2 0 5 40                  # base for fitting
python3 fit2.py base.svg ref_on_white.png insignia.svg fitted-params.json           # fit insignia
python3 trace.py reference.png officer.svg 18 20 1.0 0.2 1 3 0 5 90 insignia.svg    # final trace
node score.mjs officer.svg officer.png && python3 diff.py ref_on_white.png officer.png diff.png
```

`trace.py` arguments: `K TURD ALPHAMAX OPTTOL DILATE UPSCALE MEANSHIFT MEDIAN MINPX [OVERLAY]`.

## Iteration log

| Iteration | Change | Mean error (0-255) | Pixels off >40 |
|---|---|---|---|
| 1 | 14 colours, 1x | 6.85 | 2.55% |
| 2 | trace at 2x | 4.64 | 1.38% |
| 3 | speck merging + hand-built insignia | 4.91 | 1.53% |
| 4-5 | insignia transforms fitted; blurred metric + bounds (first fits collapsed pieces) | 4.69 | 1.41% |
| 6-8 | fully parametric insignia, cover patches against ghosts | 4.74 | 1.39% |
| 9a | trace at 3x | 4.37 | 1.10% |
| 9b | 24 colours at 3x (rejected: green speckle on the face) | 4.46 | 1.28% |
| 11 | emblem locked to grid measurement (final) | **4.41** | **1.10%** |

What's left is sub-pixel anti-aliasing along outlines, and smooth gradients (boot gloss, cape shading) that flat fills can only approximate in steps.
