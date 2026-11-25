from pathlib import Path
from PIL import Image
import numpy as np
from collections import deque

LAYERS = Path('/workspace/pivot-monthly-top5-celebration/v3/layers')
imD = Image.open(LAYERS / 'compD_fg.png').convert('RGBA')
arr = np.array(imD)
r, g, b, a = arr[:,:,0].astype(int), arr[:,:,1].astype(int), arr[:,:,2].astype(int), arr[:,:,3]
sat = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
lum = (r + g + b) / 3.0

# Only strip near-pure-white flat studio background contiguous with transparent air above crown
is_bg_like = ((lum > 224) & (sat < 14)) | (a < 20)
visited = np.zeros((900, 1600), dtype=bool)
q = deque()
for y in range(340, 445):
    for x in range(900, 1240):
        if a[y, x] < 15:
            visited[y, x] = True
            q.append((y, x))

while q:
    y, x = q.popleft()
    for dy, dx in ((-1,0),(1,0),(0,-1),(0,1)):
        ny, nx = y + dy, x + dx
        if 340 <= ny < 438 and 910 <= nx < 1230 and not visited[ny, nx]:
            if is_bg_like[ny, nx]:
                visited[ny, nx] = True
                arr[ny, nx, 3] = 0
                q.append((ny, nx))

arr[arr[:,:,3] < 12, 3] = 0
Image.fromarray(arr).save(LAYERS / 'compD_clean.png')
print("Re-cleaned compD_clean.png gently.")
