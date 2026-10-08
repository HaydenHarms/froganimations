"""Trace the officer reference into a layered SVG.
usage: python3 -I trace.py ref.png out.svg K TURD ALPHAMAX OPTTOL DILATE"""
import sys, cv2, numpy as np, potrace

ref, out = sys.argv[1], sys.argv[2]
K, TURD, AMAX, OTOL, DIL = int(sys.argv[3]), int(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6]), int(sys.argv[7])
UP = int(sys.argv[8]) if len(sys.argv) > 8 else 1          # trace at UPx resolution
SR = int(sys.argv[9]) if len(sys.argv) > 9 else 0          # mean-shift colour radius (0 = off)
MED = int(sys.argv[10]) if len(sys.argv) > 10 else 3       # label median size
MINPX = int(sys.argv[11]) if len(sys.argv) > 11 else 0     # merge label specks smaller than this (in traced px)
OVERLAY = sys.argv[12] if len(sys.argv) > 12 else ''       # hand-built SVG fragment painted on top

im = cv2.imread(ref, cv2.IMREAD_UNCHANGED)
W0, H0 = im.shape[1], im.shape[0]
if UP > 1:
    im = cv2.resize(im, (W0 * UP, H0 * UP), interpolation=cv2.INTER_CUBIC)
if SR:
    im[..., :3] = cv2.pyrMeanShiftFiltering(im[..., :3], 6 * UP, SR)
bgr = im[..., :3].astype(np.float32); a = im[..., 3]
opaque = a >= 128
H, W = a.shape

# palette from opaque pixels, in Lab for perceptual clustering
lab = cv2.cvtColor(im[..., :3], cv2.COLOR_BGR2LAB).reshape(-1, 3).astype(np.float32)
sel = lab[opaque.ravel()]
crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
cv2.setRNGSeed(1)
_, lbl, cen = cv2.kmeans(sel, K, None, crit, 4, cv2.KMEANS_PP_CENTERS)
labels = np.full(H * W, -1, np.int32); labels[opaque.ravel()] = lbl.ravel()
labels = labels.reshape(H, W)
# light cleanup: median filter on label map removes JPEG speckle
labels_m = cv2.medianBlur((labels + 1).astype(np.uint8), MED).astype(np.int32) - 1
labels_m[~opaque] = -1
labels = labels_m

def merge_specks(labels, minpx):
    """Relabel every connected component smaller than minpx to the most common label around it."""
    for _ in range(2):
        changed = 0
        for i in range(K):
            n, cc, st, _ = cv2.connectedComponentsWithStats((labels == i).astype(np.uint8), connectivity=4)
            for j in range(1, n):
                x, y, w, h, area = st[j]
                if area >= minpx: continue
                x0, y0, x1, y1 = max(x - 2, 0), max(y - 2, 0), min(x + w + 2, labels.shape[1]), min(y + h + 2, labels.shape[0])
                comp = cc[y0:y1, x0:x1] == j
                ring = cv2.dilate(comp.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & ~comp
                nb = labels[y0:y1, x0:x1][ring]; nb = nb[nb != i]
                if nb.size == 0: continue
                vals, cnts = np.unique(nb, return_counts=True); new = vals[np.argmax(cnts)]
                labels[y0:y1, x0:x1][comp] = new; changed += 1
        if not changed: break
    return labels
if MINPX: labels = merge_specks(labels, MINPX)

cen_bgr = cv2.cvtColor(cen.reshape(1, -1, 3).astype(np.uint8), cv2.COLOR_LAB2BGR).reshape(-1, 3)
hexs = ['#%02x%02x%02x' % tuple(int(v) for v in c[::-1]) for c in cen_bgr]
L = cen[:, 0]
area = np.array([(labels == i).sum() for i in range(K)])
# paint order: biggest regions first (they become the base), small details on top
order = list(np.argsort(-area))

def to_path(mask):
    bm = potrace.Bitmap(~mask)  # potracer inverts: False = ink
    plist = bm.trace(turdsize=TURD, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY,
                     alphamax=AMAX, opticurve=OTOL > 0, opttolerance=max(OTOL, 0.01))
    d = []
    for curve in plist:
        f = 1.0 / UP
        sp = curve.start_point; d.append(f'M{sp.x*f:.1f} {sp.y*f:.1f}')
        for seg in curve.segments:
            if seg.is_corner:
                d.append(f'L{seg.c.x*f:.1f} {seg.c.y*f:.1f}L{seg.end_point.x*f:.1f} {seg.end_point.y*f:.1f}')
            else:
                d.append(f'C{seg.c1.x*f:.1f} {seg.c1.y*f:.1f} {seg.c2.x*f:.1f} {seg.c2.y*f:.1f} {seg.end_point.x*f:.1f} {seg.end_point.y*f:.1f}')
        d.append('Z')
    return ''.join(d)

k = np.ones((3, 3), np.uint8)
parts = []
# base silhouette in the darkest colour so nothing shows through gaps
darkest = int(np.argmin(L))
parts.append(f'<path id="silhouette" fill="{hexs[darkest]}" d="{to_path(opaque)}"/>')
for i in order:
    if i == darkest: continue
    m = (labels == i).astype(np.uint8)
    if DIL: m = cv2.dilate(m, k, iterations=DIL)
    m &= opaque.astype(np.uint8)
    d = to_path(m.astype(bool))
    if d: parts.append(f'<path fill="{hexs[i]}" d="{d}"/>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W0} {H0}" width="{W0}" height="{H0}">\n'
       + '\n'.join(parts) + '\n' + (open(OVERLAY).read() if OVERLAY else '') + '</svg>\n')
open(out, 'w').write(svg)
print('subpaths', svg.count('M'), 'palette', ' '.join(hexs[i] for i in order), 'bytes', len(svg))
