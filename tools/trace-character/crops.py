# Side-by-side zoomed crops: reference (left) vs render (right) for the detail areas.
import sys, cv2, numpy as np
ref = cv2.imread(sys.argv[1]); got = cv2.imread(sys.argv[2]); out = sys.argv[3]
R = {'face': (390, 150, 790, 400), 'emblem': (620, 50, 730, 150), 'plaque': (600, 455, 780, 560),
     'buckle': (610, 680, 740, 790), 'boots': (330, 1150, 860, 1510), 'hands': (290, 620, 800, 800)}
names = sys.argv[4].split(',') if len(sys.argv) > 4 else list(R)
rows = []
for n in names:
    x0, y0, x1, y1 = R[n]
    a, b = ref[y0:y1, x0:x1], got[y0:y1, x0:x1]
    s = 520 / (x1 - x0)
    a = cv2.resize(a, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)
    b = cv2.resize(b, None, fx=s, fy=s, interpolation=cv2.INTER_NEAREST)
    rows.append(np.hstack([a, np.full((a.shape[0], 12, 3), 255, np.uint8), b]))
    rows.append(np.full((12, rows[-1].shape[1], 3), 255, np.uint8))
cv2.imwrite(out, np.vstack(rows))
