"""Parametric insignia: each piece is generated from a parameter vector that is fitted to the reference.
usage: python3 -I fit2.py traced_base.svg ref_on_white.png out_insignia.svg [params.json]"""
import sys, json, os, cv2, numpy as np, cairosvg
from scipy.optimize import minimize
traced, ref_path, out = sys.argv[1:4]
pfile = sys.argv[4] if len(sys.argv) > 4 else None
ref = cv2.imread(ref_path).astype(np.float32)
base = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=open(traced, 'rb').read(), background_color='white'), np.uint8), 1).astype(np.float32)
INK, WH, RED, BLUE = '#151517', '#f2f2f3', '#f0312a', '#2a54c7'

def emblem(p):
    cx, cy, rot, sx, sy, R, ring, line, gap, band, notch, hub, spw, spl = p
    sp = ''.join(f'<rect x="{-spw/2:.2f}" y="{-spl:.2f}" width="{spw:.2f}" height="{spl:.2f}" transform="rotate({a})"/>' for a in range(0, 360, 60))
    rb = R - ring - line - gap - band / 2
    nt = ''.join(f'<rect x="{-notch/2:.2f}" y="{-(rb+band/2+0.6):.2f}" width="{notch:.2f}" height="{band+1.2:.2f}" transform="rotate({a})"/>' for a in range(0, 360, 60))
    return (f'<g id="emblem" transform="translate({cx:.2f} {cy:.2f}) rotate({rot:.2f}) scale({sx:.3f} {sy:.3f})">'
            f'<circle r="{R+1.2:.2f}" fill="{INK}"/><circle r="{R:.2f}" fill="{WH}"/>'
            f'<circle r="{R-ring-line/2:.2f}" fill="none" stroke="{INK}" stroke-width="{line:.2f}"/>'
            f'<circle r="{rb:.2f}" fill="none" stroke="{INK}" stroke-width="{band:.2f}"/>'
            f'<g fill="{WH}">{nt}</g><g fill="{INK}"><circle r="{hub:.2f}"/>{sp}</g></g>')

def button(p, id_):
    cx, cy, r, ox, oy, hl = p
    return (f'<g id="{id_}"><circle cx="{cx:.2f}" cy="{cy:.2f}" r="{r+1.6:.2f}" fill="#1b1b1d"/>'
            f'<circle cx="{cx+ox:.2f}" cy="{cy+oy:.2f}" r="{r:.2f}" fill="#a6a6a8"/>'
            f'<path d="M{cx+ox+r*np.cos(np.radians(-100)):.2f} {cy+oy+r*np.sin(np.radians(-100)):.2f} A{r:.2f} {r:.2f} 0 0 1 {cx+ox+r*np.cos(np.radians(-10)):.2f} {cy+oy+r*np.sin(np.radians(-10)):.2f}" '
            f'fill="none" stroke="#ececee" stroke-width="{hl:.2f}" stroke-linecap="round"/></g>')

def plaque(p):
    a, b, c, d, e, f, bw, sep, gapc, top = p
    cw = (100 - 2 * bw - 2 * 2 - 3 * gapc) / 4
    xs = [bw + 2 + k * (cw + gapc) for k in range(4)]
    h1 = 50 - sep / 2 - top; h2 = 100 - top - (50 + sep / 2)
    reds = ''.join(f'<rect x="{x:.2f}" y="{top:.2f}" width="{cw:.2f}" height="{h1-1.5:.2f}"/>' for x in xs)
    blues = ''.join(f'<rect x="{x:.2f}" y="{50+sep/2+1.5:.2f}" width="{cw:.2f}" height="{h2-1.5:.2f}"/>' for x in xs)
    return (f'<g id="rank-plaque" transform="matrix({a:.4f} {b:.4f} {c:.4f} {d:.4f} {e:.2f} {f:.2f})">'
            f'<rect x="-2" y="-2.5" width="104" height="105" fill="{INK}"/><rect width="100" height="100" fill="{WH}"/>'
            f'<rect x="{bw:.2f}" y="{bw:.2f}" width="{100-2*bw:.2f}" height="{100-2*bw:.2f}" fill="{INK}"/>'
            f'<rect x="{bw:.2f}" y="{50-sep/2:.2f}" width="{100-2*bw:.2f}" height="{sep:.2f}" fill="{WH}"/>'
            f'<g fill="{RED}">{reds}</g><g fill="{BLUE}">{blues}</g></g>')

def cylinder(p, id_):
    cx, ty, rot, capw, caph, bw, bh, footw, footh, hlx, hlw, shw, bandy = p
    hw, cw, fw = bw / 2, capw / 2, footw / 2
    outline = (f'M{-cw} 0 H{cw} V{caph} H{hw} V{caph+bh} H{fw} V{caph+bh+footh} H{-fw} V{caph+bh} H{-hw} V{caph} H{-cw} Z')
    return (f'<g id="{id_}" transform="translate({cx:.2f} {ty:.2f}) rotate({rot:.2f})">'
            f'<path d="{outline}" fill="#8e8f91" stroke="{INK}" stroke-width="2" stroke-linejoin="round"/>'
            f'<rect x="{hlx:.2f}" y="{caph:.2f}" width="{hlw:.2f}" height="{bh:.2f}" fill="#e8e8ea"/>'
            f'<rect x="{-cw*0.5:.2f}" y="0.8" width="{cw*0.8:.2f}" height="{caph-0.8:.2f}" fill="#e8e8ea"/>'
            f'<rect x="{hw-shw:.2f}" y="{caph:.2f}" width="{shw:.2f}" height="{bh:.2f}" fill="#5e5f61"/>'
            f'<path d="M{-hw:.2f} {caph+bandy:.2f} H{hw:.2f}" stroke="#2c2c2e" stroke-width="1.4"/></g>')

PIECES = {
    'emblem': (emblem, (634, 56, 724, 144), [676.8, 99.8, -3, 0.865, 0.955, 33.65, 3.0, 1.4, 0.5, 5.2, 10.85, 10.4, 6.4, 19.5]),
    'hat-button': (lambda p: button(p, 'hat-button'), (486, 153, 520, 187), [503, 169, 9, 0, 0, 2.6]),
    'buckle-button': (lambda p: button(p, 'buckle-button'), (668, 714, 718, 764), [692, 738.5, 11.2, 2, -2, 2.4]),
    'rank-plaque': (plaque, (648, 463, 748, 548), [0.625, 0.138, 0.118, 0.488, 661.5, 474.5, 4.5, 5, 2.6, 8]),
    'cyl-left': (lambda p: cylinder(p, 'cyl-left'), (616, 462, 656, 528), [636, 475.5, -5, 9, 6.5, 16, 30, 11, 5.5, -3.6, 4.4, 3.4, 15]),
    'cyl-right': (lambda p: cylinder(p, 'cyl-right'), (731, 491, 769, 556), [748.5, 503.5, -4, 9, 6.5, 16, 30, 11, 5.5, -3.6, 4.4, 3.4, 15]),
}

# Fixed patches that hide the traced original under each piece, in the median colour of the fabric around it.
def ring_colour(mask_fn, box):
    x0, y0, x1, y1 = box
    yy, xx = np.mgrid[y0:y1, x0:x1]
    inside = mask_fn(xx, yy, 0); outside = mask_fn(xx, yy, 3) & ~inside
    px = ref[y0:y1, x0:x1][outside]
    b, g, r = np.median(px, axis=0)
    return '#%02x%02x%02x' % (int(r), int(g), int(b))
def ell(cx, cy, rx, ry):
    return lambda xx, yy, g: ((xx - cx) / (rx + g)) ** 2 + ((yy - cy) / (ry + g)) ** 2 <= 1
def poly(pts):
    pts = np.array(pts, np.float32)
    def f(xx, yy, g):
        c = pts.mean(0); P = c + (pts - c) * (1 + g / 25)
        out = np.zeros(xx.shape, bool)
        m = np.zeros((xx.shape[0], xx.shape[1]), np.uint8)
        cv2.fillPoly(m, [np.round(P - [xx[0, 0], yy[0, 0]]).astype(np.int32)], 1)
        return m.astype(bool)
    return f
PATCHES = {
    'emblem': ('ellipse', (676.8, 99.8, 32, 35)),
    'hat-button': ('ellipse', (503, 169.5, 11.5, 11.5)),
    'buckle-button': ('ellipse', (692.5, 738.5, 16, 16)),
    'rank-plaque': ('poly', [(660, 472), (727, 487), (737, 540), (671, 526)]),
    'cyl-left': ('poly', [(628, 473), (640, 472), (647, 519), (633, 521)]),
    'cyl-right': ('poly', [(740, 501), (752, 500), (758, 545), (744, 547)]),
}
def patch_svg(name, box):
    kind, g = PATCHES[name]
    if kind == 'ellipse':
        col = ring_colour(ell(*g), box)
        return f'<ellipse cx="{g[0]}" cy="{g[1]}" rx="{g[2]}" ry="{g[3]}" fill="{col}"/>'
    col = ring_colour(poly(g), box)
    return f'<polygon points="{" ".join(f"{x},{y}" for x, y in g)}" fill="{col}"/>'

def raster(frag, box):
    x0, y0, x1, y1 = box
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {x1-x0} {y1-y0}" width="{(x1-x0)*2}" height="{(y1-y0)*2}">{frag}</svg>'
    a = cv2.imdecode(np.frombuffer(cairosvg.svg2png(bytestring=svg.encode()), np.uint8), cv2.IMREAD_UNCHANGED).astype(np.float32)
    return cv2.resize(a, (x1 - x0, y1 - y0), interpolation=cv2.INTER_AREA)

BL = lambda im: cv2.GaussianBlur(im, (0, 0), 1.1)
def err(build, box, p, lo=None, hi=None):
    x0, y0, x1, y1 = box
    if lo is not None and (np.any(p < lo) or np.any(p > hi)): return 1e3
    try: a = raster(build(p), box)
    except Exception: return 1e3
    al = a[..., 3:4] / 255
    comp = a[..., :3] * al + base[y0:y1, x0:x1] * (1 - al)
    return float(np.abs(BL(comp) - BL(ref[y0:y1, x0:x1])).mean())

params = {}   # always start from the measured values; bounds are relative to them
frags = []
for name, (build0, box, p0) in PIECES.items():
    patch = patch_svg(name, box)
    build = (lambda b, pt: (lambda p: pt + b(p)))(build0, patch)
    p0 = np.array(p0, float)
    lim = np.maximum(np.abs(p0) * 0.25, 2.0)
    lim[np.abs(p0) > 100] = 5.0                         # absolute coordinates: +-5 px
    if name == 'rank-plaque': lim[:4] = np.abs(p0[:4]) * 0.12
    if name == 'emblem': lim[2] = 12; lim[3:5] = 0.12; lim[5:] = np.abs(p0[5:]) * 0.10   # structure measured by eye; fit placement
    lo, hi = p0 - lim, p0 + lim
    x0, y0, x1, y1 = box
    eb = np.abs(BL(base[y0:y1, x0:x1]) - BL(ref[y0:y1, x0:x1])).mean()
    e0 = err(build, box, p0)
    best_p, best_e = p0, e0
    LOCKED = {'emblem'}   # placed from the 9x grid comparison; the blurred metric drifts on the hat's shading
    for rnd in range(0 if name in LOCKED else 3):
        steps = np.maximum(np.abs(best_p) * 0.04, 0.6) * (0.5 ** rnd)
        steps[np.abs(best_p) > 100] = 1.5 * (0.5 ** rnd)           # absolute coordinates: pixel steps
        simplex = np.vstack([best_p] + [best_p + np.eye(len(best_p))[k] * steps[k] for k in range(len(best_p))])
        r = minimize(lambda p: err(build, box, p, lo, hi), best_p, method='Nelder-Mead',
                     options={'maxiter': 2500, 'xatol': 0.005, 'fatol': 0.002, 'initial_simplex': simplex, 'adaptive': True})
        if r.fun < best_e: best_p, best_e = r.x, r.fun
    params[name] = best_p.tolist()
    print(f'{name:14s} traced-only {eb:6.2f} | start {e0:6.2f} -> fitted {best_e:6.2f}', flush=True)
    frags.append(build(best_p))
open(out, 'w').write('<g id="insignia">\n' + '\n'.join(frags) + '\n</g>\n')
if pfile: json.dump(params, open(pfile, 'w'), indent=1)
