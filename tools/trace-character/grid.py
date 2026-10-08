# Zoomed crop with a labelled pixel grid every `step` px, for reading exact coordinates.
import sys, cv2, numpy as np
img = cv2.imread(sys.argv[1]); x0, y0, x1, y1, step, z = map(int, sys.argv[2:8]); out = sys.argv[8]
c = cv2.resize(img[y0:y1, x0:x1], None, fx=z, fy=z, interpolation=cv2.INTER_NEAREST)
pad = 40; canvas = np.full((c.shape[0] + pad, c.shape[1] + pad, 3), 255, np.uint8); canvas[pad:, pad:] = c
for x in range((x0 // step + 1) * step, x1, step):
    X = pad + (x - x0) * z; cv2.line(canvas, (X, pad), (X, canvas.shape[0]), (0, 200, 255), 1)
    cv2.putText(canvas, str(x), (X - 14, 26), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
for y in range((y0 // step + 1) * step, y1, step):
    Y = pad + (y - y0) * z; cv2.line(canvas, (pad, Y), (canvas.shape[1], Y), (0, 200, 255), 1)
    cv2.putText(canvas, str(y), (2, Y + 4), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
cv2.imwrite(out, canvas)
