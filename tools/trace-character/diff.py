import sys, cv2, numpy as np
ref = cv2.imread(sys.argv[1]).astype(np.int16); got = cv2.imread(sys.argv[2]).astype(np.int16)
d = np.abs(ref - got).max(axis=2)
fg = (ref < 250).any(axis=2) | (got < 250).any(axis=2)
mae = d[fg].mean(); bad = (d[fg] > 40).mean() * 100
print(f'MAE {mae:.2f}  pixels off>40: {bad:.2f}%  of {fg.sum()} fg px')
heat = np.clip(d * 3, 0, 255).astype(np.uint8)
cv2.imwrite(sys.argv[3], cv2.applyColorMap(heat, cv2.COLORMAP_INFERNO))
