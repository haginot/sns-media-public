from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

LAYERS = Path('/workspace/pivot-monthly-top5-celebration/v3/layers')
QC = Path('/workspace/pivot-monthly-top5-celebration/v3/qc')

# 1. Clean D
imD = Image.open(LAYERS / 'compD_fg.png').convert('RGBA')
arrD = np.array(imD)
r, g, b = arrD[:,:,0].astype(int), arrD[:,:,1].astype(int), arrD[:,:,2].astype(int)
sat = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
lum = (r + g + b) / 3.0
Y, X = np.ogrid[:900, :1600]
crown_zone = (Y < 470) & (X > 920) & (X < 1210)
arrD[crown_zone & (lum > 205) & (sat < 22), 3] = 0
arrD[arrD[:,:,3] < 12, 3] = 0
Image.fromarray(arrD).save(LAYERS / 'compD_clean.png')

# 2. Clean A
imA = Image.open(LAYERS / 'compA_fg.png').convert('RGBA')
arrA = np.array(imA)
arrA[arrA[:,:,3] < 12, 3] = 0
Image.fromarray(arrA).save(LAYERS / 'compA_clean.png')

# 3. Clean C full + foreground overlays (glasses & foreground Jollys)
imC = Image.open(LAYERS / 'compC_fg.png').convert('RGBA')
arrC = np.array(imC)
arrC[arrC[:,:,3] < 10, 3] = 0
imC = Image.fromarray(arrC)
imC.save(LAYERS / 'compC_clean.png')

def make_overlay(poly, out_name, blur=3.0):
    m = Image.new('L', (1600, 900), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    ma = np.array(m).astype(float) / 255.0
    a = np.array(imC).copy()
    a[:,:,3] = (a[:,:,3].astype(float) * ma).astype(np.uint8)
    Image.fromarray(a).save(LAYERS / out_name)

# Foreground bottom-right Jolly + coupe glass (cleanly separated from mid-right Jolly)
make_overlay([
    (1030, 625),
    (1225, 560),
    (1325, 575),
    (1412, 650),
    (1472, 760),
    (1515, 900),
    (1030, 900),
], 'C_fg_right.png', blur=2.0)

# Foreground bottom-left Jolly's coupe glass + raised arm (blends smoothly into body in compC_clean)
make_overlay([
    (255, 560),
    (295, 450),
    (440, 450),
    (438, 558),
    (382, 578),
    (370, 640),
    (342, 710),
    (255, 710),
], 'C_fg_left_glass.png', blur=4.0)

# Foreground sitting Jolly's flute glass + paw (blends smoothly into sitting Jolly)
make_overlay([
    (530, 580),
    (630, 580),
    (630, 795),
    (530, 795),
], 'C_fg_sitting_flute.png', blur=4.0)

# Also C_top_jollys (top-left and top-right floating Jollys) so they can sit IN FRONT of back laurel rings if desired
make_overlay([
    (0, 0),
    (400, 0),
    (400, 445),
    (160, 435),
    (0, 442),
], 'C_top_left.png', blur=2.0)

make_overlay([
    (1180, 0),
    (1600, 0),
    (1600, 425),
    (1350, 425),
    (1180, 380),
], 'C_top_right.png', blur=2.0)

print("Generated clean layers for A, C, D.")
