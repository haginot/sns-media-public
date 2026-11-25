from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

LAYERS = Path('/workspace/pivot-monthly-top5-celebration/v3/layers')

# 1. Extract A_right_paw.png for Z=5 overlap over medallion ribbon tails
imA = Image.open(LAYERS / 'compA_clean.png').convert('RGBA')
m_paw = Image.new('L', (1600, 900), 0)
ImageDraw.Draw(m_paw).polygon([
    (1118, 400),
    (1225, 400),
    (1225, 515),
    (1118, 515),
], fill=255)
m_paw = m_paw.filter(ImageFilter.GaussianBlur(3.0))
a_paw = np.array(imA).copy()
a_paw[:,:,3] = (a_paw[:,:,3].astype(float) * (np.array(m_paw).astype(float) / 255.0)).astype(np.uint8)
Image.fromarray(a_paw).save(LAYERS / 'A_right_paw.png')

# 2. Fix C_fg_sitting_flute.png cleanly (strictly flute + paw x>=548)
imC = Image.open(LAYERS / 'compC_clean.png').convert('RGBA')
m_flute = Image.new('L', (1600, 900), 0)
ImageDraw.Draw(m_flute).polygon([
    (548, 575),
    (630, 575),
    (630, 795),
    (552, 795),
    (552, 725),
    (548, 665),
], fill=255)
m_flute = m_flute.filter(ImageFilter.GaussianBlur(2.0))
a_flute = np.array(imC).copy()
a_flute[:,:,3] = (a_flute[:,:,3].astype(float) * (np.array(m_flute).astype(float) / 255.0)).astype(np.uint8)
Image.fromarray(a_flute).save(LAYERS / 'C_fg_sitting_flute.png')

# 3. Gentle 0.8px alpha smooth on D crown edge (y < 450)
imD = Image.open(LAYERS / 'compD_clean.png').convert('RGBA')
arrD = np.array(imD)
alpha_img = Image.fromarray(arrD[:,:,3])
alpha_soft = alpha_img.filter(ImageFilter.GaussianBlur(0.6))
arr_soft = np.array(alpha_soft)
# Apply soft edge only in the top crown band y < 445 where alpha < 245
band = np.zeros((900, 1600), dtype=bool)
band[:445, :] = True
edge = band & (arrD[:,:,3] < 240)
arrD[edge, 3] = arr_soft[edge]
Image.fromarray(arrD).save(LAYERS / 'compD_clean.png')
print("Polished A_right_paw, C_fg_sitting_flute, and compD_clean.")
