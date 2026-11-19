#!/usr/bin/env python3
"""Lab-notebook backgrounds for the pstack hands-on series.

Three text-free variants, each in 1920x1080 (video / 16:9) and
1280x670 (note eyecatch). Built procedurally with numpy / PIL / scipy
so the paper grain, grid and stains look photographed, not generated.

    A  warm off-white 5 mm graph paper
    B  night-shift navy graph paper with a desk-lamp glow
    C  engineering-pad green-grey with a soft dawn wash

A large clean central field (~60% of the canvas) is kept free of
stains, tape and heavy lighting so screenshots can sit on top.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter, zoom

OUT = Path(__file__).resolve().parent
SIZES = ((1920, 1080), (1280, 670))
# 5 mm at a ~320 mm-wide page: 30 px at 1920, 20 px at 1280.
CELL_DIV = 64
MAJOR_EVERY = 5
CENTER_FRAC = 0.60


# ---------------------------------------------------------------------------
# small utilities
# ---------------------------------------------------------------------------

def srgb_to_linear(c: np.ndarray) -> np.ndarray:
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c: np.ndarray) -> np.ndarray:
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, c * 12.92, 1.055 * np.power(c, 1.0 / 2.4) - 0.055)


def hex_rgb(h: str) -> np.ndarray:
    h = h.lstrip("#")
    return np.array(
        [int(h[i : i + 2], 16) / 255.0 for i in (0, 2, 4)], dtype=np.float32
    )


def smoothstep(x: np.ndarray) -> np.ndarray:
    x = np.clip(x, 0.0, 1.0)
    return x * x * (3.0 - 2.0 * x)


def to_uint8_dither(img: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """Convert float sRGB [0, 1] to uint8 with triangular dither to kill banding."""
    dither = rng.uniform(-0.5 / 255.0, 0.5 / 255.0, img.shape).astype(np.float32)
    out = np.clip(img + dither, 0.0, 1.0)
    return (out * 255.0 + 0.5).astype(np.uint8)


def mesh(h: int, w: int):
    yy, xx = np.ogrid[0:h, 0:w]
    return yy.astype(np.float32), xx.astype(np.float32)


def edge_weight(h: int, w: int, center_frac: float = CENTER_FRAC, softness: float = 90.0) -> np.ndarray:
    """0 in the central ~60% rectangle, 1 toward the edges. Soft falloff."""
    yy, xx = mesh(h, w)
    cx, cy = w * 0.5, h * 0.5
    half_w = w * center_frac * 0.5
    half_h = h * center_frac * 0.5
    dx = np.maximum(np.abs(xx - cx) - half_w, 0.0)
    dy = np.maximum(np.abs(yy - cy) - half_h, 0.0)
    dist = np.sqrt(dx * dx + dy * dy)
    return smoothstep(np.clip(dist / softness, 0.0, 1.0))


def upsample_noise(h: int, w: int, scale: int, rng: np.random.Generator) -> np.ndarray:
    sh = max(1, int(round(h / scale)))
    sw = max(1, int(round(w / scale)))
    n = rng.normal(0.0, 1.0, (sh, sw)).astype(np.float32)
    n = zoom(n, (h / sh, w / sw), order=3)
    return n[:h, :w]


# ---------------------------------------------------------------------------
# paper body
# ---------------------------------------------------------------------------

def paper_body(
    h: int,
    w: int,
    rng: np.random.Generator,
    base: np.ndarray,
    mottle_amp: float,
    mottle_tint: np.ndarray,
    grain_amp: float,
    fiber_amp: float,
    fleck_density: float,
    fleck_color: np.ndarray,
) -> np.ndarray:
    """Toned paper with mottling, pulp fibers, fine grain and sparse flecks."""
    img = np.empty((h, w, 3), dtype=np.float32)
    img[...] = base

    # Tight, quiet pulp mottling — paper tooth, not watercolor clouds.
    mottle = (
        upsample_noise(h, w, 7, rng) * 0.50
        + upsample_noise(h, w, 4, rng) * 0.35
        + upsample_noise(h, w, 14, rng) * 0.15
    )
    mottle = gaussian_filter(mottle, 0.8)
    mottle = (mottle - mottle.mean()) / (mottle.std() + 1e-6)
    img += (mottle * mottle_amp)[..., None] * mottle_tint

    # Anisotropic fiber (mostly horizontal, a few degrees of drift).
    fiber = rng.normal(0.0, 1.0, (h, w)).astype(np.float32)
    fiber = gaussian_filter(fiber, sigma=(0.45, 3.2))
    # A second, slightly diagonal pass for a less "digital blur" feel.
    fiber2 = rng.normal(0.0, 1.0, (h, max(8, w // 3))).astype(np.float32)
    fiber2 = gaussian_filter(fiber2, sigma=(0.45, 2.4))
    fiber2 = zoom(fiber2, (1.0, w / fiber2.shape[1]), order=1)[:h, :w]
    # Shear a little so fibers are not perfectly axis-aligned.
    yy, xx = mesh(h, w)
    shift = (0.018 * yy).astype(np.int32)
    xs = np.clip(np.arange(w, dtype=np.int32)[None, :] - shift, 0, w - 1)
    fiber = fiber[np.arange(h)[:, None], xs]
    fiber = 0.7 * fiber + 0.3 * fiber2
    fiber = (fiber - fiber.mean()) / (fiber.std() + 1e-6)
    img += (fiber * fiber_amp)[..., None]

    # Fine grain / tooth of the paper.
    grain = rng.normal(0.0, 1.0, (h, w)).astype(np.float32)
    grain = gaussian_filter(grain, 0.45)
    grain = (grain - grain.mean()) / (grain.std() + 1e-6)
    # A touch of chroma noise so it does not look like a luma overlay.
    chroma = rng.normal(0.0, 1.0, (h, w, 3)).astype(np.float32)
    chroma = gaussian_filter(chroma, (0.4, 0.4, 0.0))
    img += (grain * grain_amp)[..., None] + chroma * (grain_amp * 0.25)

    # Sparse pulp flecks / dirt, tiny and mostly near mid-tones of the paper.
    n_flecks = int(h * w * fleck_density)
    if n_flecks:
        fy = rng.integers(0, h, n_flecks)
        fx = rng.integers(0, w, n_flecks)
        strength = rng.uniform(0.04, 0.18, n_flecks).astype(np.float32)
        for i in range(n_flecks):
            y, x = int(fy[i]), int(fx[i])
            img[y, x] = (1.0 - strength[i]) * img[y, x] + strength[i] * fleck_color
            if rng.random() < 0.35 and y + 1 < h:
                img[y + 1, x] = (1.0 - strength[i] * 0.5) * img[y + 1, x] + strength[i] * 0.5 * fleck_color

    return np.clip(img, 0.0, 1.0)


def apply_grid(
    img: np.ndarray,
    cell: int,
    minor_rgb: np.ndarray,
    minor_a: float,
    major_rgb: np.ndarray,
    major_a: float,
    major_width: int = 2,
) -> np.ndarray:
    """Crisp axis-aligned graph paper. Major lines every MAJOR_EVERY cells."""
    h, w, _ = img.shape
    # Draw onto a separate layer so intersections do not double-darken harshly,
    # then composite once. Majors overwrite minors where they coincide.
    layer = np.zeros((h, w, 3), dtype=np.float32)
    alpha = np.zeros((h, w), dtype=np.float32)

    def stroke_v(x0: int, width: int, color: np.ndarray, a: float) -> None:
        x1 = min(w, x0 + width)
        if x0 >= w or x1 <= 0:
            return
        x0c = max(0, x0)
        layer[:, x0c:x1] = color
        alpha[:, x0c:x1] = a

    def stroke_h(y0: int, width: int, color: np.ndarray, a: float) -> None:
        y1 = min(h, y0 + width)
        if y0 >= h or y1 <= 0:
            return
        y0c = max(0, y0)
        layer[y0c:y1, :] = color
        alpha[y0c:y1, :] = a

    # Minors first, majors on top.
    xs = list(range(0, w, cell))
    ys = list(range(0, h, cell))
    for i, x in enumerate(xs):
        if i % MAJOR_EVERY == 0:
            continue
        stroke_v(x, 1, minor_rgb, minor_a)
    for i, y in enumerate(ys):
        if i % MAJOR_EVERY == 0:
            continue
        stroke_h(y, 1, minor_rgb, minor_a)
    for i, x in enumerate(xs):
        if i % MAJOR_EVERY != 0:
            continue
        # Center a 2 px major on the grid line as much as possible.
        x0 = x if major_width == 1 else max(0, x - (major_width // 2) + 1)
        # Keep the first major (x == 0) flush with the left edge.
        if x == 0:
            x0 = 0
        stroke_v(x0, major_width, major_rgb, major_a)
    for i, y in enumerate(ys):
        if i % MAJOR_EVERY != 0:
            continue
        y0 = y if major_width == 1 else max(0, y - (major_width // 2) + 1)
        if y == 0:
            y0 = 0
        stroke_h(y0, major_width, major_rgb, major_a)

    a = alpha[..., None]
    return np.clip(img * (1.0 - a) + layer * a, 0.0, 1.0)


def apply_margin_line(
    img: np.ndarray,
    x: int,
    color: np.ndarray,
    alpha: float,
    width: int = 2,
) -> np.ndarray:
    h, w, _ = img.shape
    x0 = max(0, min(w - width, x))
    img = img.copy()
    img[:, x0 : x0 + width] = img[:, x0 : x0 + width] * (1.0 - alpha) + color * alpha
    return img


def binding_and_wear(
    img: np.ndarray,
    rng: np.random.Generator,
    shadow_rgb: np.ndarray,
    yellow_rgb: np.ndarray,
    shadow_amp: float,
    yellow_amp: float,
    left_bind: bool = True,
) -> np.ndarray:
    """Notebook-spine shadow on one edge, slightly aged corners, faint vignette."""
    h, w, _ = img.shape
    yy, xx = mesh(h, w)
    ew = edge_weight(h, w, softness=max(70.0, w * 0.06))

    # Spine falloff — a soft cylindrical shade along the left (or right) edge.
    if left_bind:
        t = np.clip(xx / (w * 0.085), 0.0, 1.0)
    else:
        t = np.clip((w - 1 - xx) / (w * 0.085), 0.0, 1.0)
    bind = (1.0 - smoothstep(t)) * shadow_amp
    # A hint of a second, tighter contact shadow.
    t2 = np.clip(xx / (w * 0.018) if left_bind else (w - 1 - xx) / (w * 0.018), 0.0, 1.0)
    bind = np.maximum(bind, (1.0 - smoothstep(t2)) * shadow_amp * 1.4)

    img = img * (1.0 - bind[..., None]) + shadow_rgb * bind[..., None]

    # Corner aging (distance from each corner).
    corners = [
        (0.0, 0.0),
        (w - 1.0, 0.0),
        (0.0, h - 1.0),
        (w - 1.0, h - 1.0),
    ]
    age = np.zeros((h, w), dtype=np.float32)
    radius = 0.22 * min(h, w)
    for cx, cy in corners:
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        age = np.maximum(age, np.clip(1.0 - d / radius, 0.0, 1.0) ** 1.6)
    age *= yellow_amp
    age *= ew  # keep the center clean
    img = img * (1.0 - age[..., None]) + yellow_rgb * age[..., None]

    # Very soft vignette, edges only, so the page feels lit from above.
    vx = np.minimum(xx / (w * 0.04), (w - 1 - xx) / (w * 0.04))
    vy = np.minimum(yy / (h * 0.05), (h - 1 - yy) / (h * 0.05))
    vig = 1.0 - 0.07 * (1.0 - smoothstep(np.clip(np.minimum(vx, vy), 0.0, 1.0)))
    img = img * vig[..., None]

    return np.clip(img, 0.0, 1.0)


# ---------------------------------------------------------------------------
# edge decorations
# ---------------------------------------------------------------------------

def coffee_ring(
    h: int,
    w: int,
    cx: float,
    cy: float,
    radius: float,
    rng: np.random.Generator,
    color: np.ndarray,
    strength: float = 0.32,
) -> tuple[np.ndarray, np.ndarray]:
    """Imperfect ring plus a faint inner wash and a couple of droplets."""
    yy, xx = mesh(h, w)
    ang = np.arctan2(yy - cy, xx - cx)
    r_var = radius * (
        1.0
        + 0.045 * np.sin(ang * 3.0 + 0.5)
        + 0.03 * np.sin(ang * 5.0 + 1.4)
        + 0.02 * np.sin(ang * 2.0 + 2.3)
    )
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    thick = radius * 0.075
    ring = np.exp(-0.5 * ((dist - r_var) / thick) ** 2)
    # Break the ring in places so it does not look stamped.
    fade = 0.50 + 0.50 * np.sin(ang * 2.0 + 0.9) * (0.65 + 0.35 * np.sin(ang * 7.0 + 0.2))
    fade = np.clip(fade, 0.08, 1.0)
    # Slight thickness noise.
    n = upsample_noise(h, w, 6, rng)
    n = (n - n.mean()) / (n.std() + 1e-6)
    ring = ring * (0.88 + 0.12 * np.clip(n, -1.5, 1.5))
    inner = np.clip((r_var - dist) / (r_var + 1e-6), 0.0, 1.0) ** 1.35 * 0.13

    alpha = np.clip(ring * fade * strength + inner * strength * 0.7, 0.0, 1.0)

    # Satellite droplets just outside the ring.
    for _ in range(3):
        a = float(rng.uniform(-np.pi, np.pi))
        rr = radius * float(rng.uniform(1.05, 1.35))
        dx, dy = rr * np.cos(a), rr * np.sin(a)
        drop_r = radius * float(rng.uniform(0.03, 0.07))
        dd = np.sqrt((xx - (cx + dx)) ** 2 + (yy - (cy + dy)) ** 2)
        drop = np.clip(1.0 - dd / drop_r, 0.0, 1.0) ** 1.2
        alpha = np.maximum(alpha, drop * strength * float(rng.uniform(0.35, 0.7)))

    alpha = gaussian_filter(alpha, 0.6)
    rgb = np.empty((h, w, 3), dtype=np.float32)
    rgb[...] = color
    return rgb, alpha


def tape_piece(
    h: int,
    w: int,
    cx: float,
    cy: float,
    tw: float,
    th: float,
    angle_deg: float,
    color: np.ndarray,
    rng: np.random.Generator,
    opacity: float = 0.38,
) -> tuple[np.ndarray, np.ndarray]:
    """Translucent masking-tape rectangle with slightly grimy edges and wrinkles."""
    yy, xx = mesh(h, w)
    ang = np.deg2rad(angle_deg)
    dx, dy = xx - cx, yy - cy
    rx = dx * np.cos(ang) + dy * np.sin(ang)
    ry = -dx * np.sin(ang) + dy * np.cos(ang)
    # Slightly ragged short ends, like a torn piece of masking tape.
    end_wave = 2.2 * np.sin(ry / 7.0 + 0.4) + 1.1 * np.sin(ry / 3.2 + 1.1)
    ax = np.abs(rx) - (tw * 0.5 + end_wave)
    ay = np.abs(ry) - th * 0.5
    # Soft-edged box SDF.
    inside = np.maximum(ax, ay)
    sdf = np.minimum(inside, 0.0) + np.sqrt(np.maximum(ax, 0.0) ** 2 + np.maximum(ay, 0.0) ** 2)
    alpha = smoothstep(np.clip(0.5 - sdf / 2.2, 0.0, 1.0))

    # Lengthwise wrinkles / stretch marks.
    wrinkle = 0.82 + 0.18 * np.sin(rx / 16.0 + 0.4 * np.sin(ry / 6.0))
    wrinkle *= 0.94 + 0.06 * np.sin(rx / 7.0)
    # Adhesive edge line, slightly darker and a bit irregular.
    edge = np.exp(-0.5 * (sdf / 1.6) ** 2) * (sdf > -3.5)
    n = upsample_noise(h, w, 5, rng)
    n = (n - n.mean()) / (n.std() + 1e-6)
    edge = edge * (0.85 + 0.15 * np.clip(n, -1.0, 1.0))

    rgb = np.empty((h, w, 3), dtype=np.float32)
    rgb[...] = color
    # Slightly warmer / dirtier along the adhesive edge.
    dirt = hex_rgb("#8A6A3A")
    rgb = rgb * (1.0 - 0.22 * edge[..., None]) + dirt * (0.22 * edge[..., None])
    # Wrinkle as a mild brightness modulation.
    rgb = np.clip(rgb * wrinkle[..., None], 0.0, 1.0)

    alpha = alpha * opacity * (0.92 + 0.08 * wrinkle)
    alpha = gaussian_filter(alpha, 0.4)
    return rgb, np.clip(alpha, 0.0, 1.0)


def composite(img: np.ndarray, rgb: np.ndarray, alpha: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    a = alpha if mask is None else alpha * mask
    return np.clip(img * (1.0 - a[..., None]) + rgb * a[..., None], 0.0, 1.0)


def composite_tape(img: np.ndarray, rgb: np.ndarray, alpha: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    """Translucent tape: tint and slightly multiply so the grid still shows."""
    a = (alpha if mask is None else alpha * mask)[..., None]
    tinted = np.clip(img * (0.62 + 0.38 * rgb / (np.mean(rgb) + 1e-6)), 0.0, 1.0)
    # A little body so the tape still reads as a layer, not just a stain.
    body = np.clip(0.55 * tinted + 0.45 * rgb, 0.0, 1.0)
    return np.clip(img * (1.0 - a) + body * a, 0.0, 1.0)


def lamp_glow(h: int, w: int, img: np.ndarray) -> np.ndarray:
    """Warm desk-lamp pool in the upper-right.

    Pure radial falloff — no rectangular mask — so the glow reads as a lamp
    and the central well stays almost even navy for screenshots.
    """
    yy, xx = mesh(h, w)
    # Lamp just off the top-right corner of the desk.
    lx, ly = w * 1.06, h * -0.10
    dist = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2)
    # Wide pool + tighter core. At the image center, pool is ~3–4%.
    pool = np.exp(-((dist / (0.40 * w)) ** 2))
    core = np.exp(-((dist / (0.16 * w)) ** 2))
    # A little grain in the glow kills any residual banding.
    # (Deterministic-ish from the pixel grid, no extra rng needed.)
    dither = 1.0 + 0.012 * np.sin(xx * 0.37 + yy * 0.19) * np.sin(xx * 0.11 - yy * 0.29)
    pool = pool * dither
    core = core * dither

    # Mid-glow is a slightly warm lit navy; the core is tungsten-amber.
    # Keep the pool compact so the center stays even and we do not get a
    # muddy brown wall.
    lit = hex_rgb("#4A453C")
    warm = hex_rgb("#E8B56A")
    mid = (pool * 0.30)[..., None]
    hot = (core * 0.36)[..., None]
    lift = (pool * 0.14)[..., None] * hex_rgb("#FFD8A0")
    img = img * (1.0 - mid) + lit * mid
    img = img + (1.0 - img) * lift
    img = img * (1.0 - hot) + warm * hot
    return np.clip(img, 0.0, 1.0)


def dawn_wash(h: int, w: int, img: np.ndarray) -> np.ndarray:
    """Soft sunrise from the top-right, cooler residual at the lower left.

    The warmth is a radial bloom from the corner, so the central well stays
    almost even and there is no rectangular lighting mask.
    """
    yy, xx = mesh(h, w)
    lx, ly = w * 1.05, h * -0.12
    dist = np.sqrt((xx - lx) ** 2 + (yy - ly) ** 2)
    bloom = np.exp(-((dist / (0.46 * w)) ** 2))
    # A shallower cool wash from the opposite corner, very quiet.
    cx, cy = w * -0.05, h * 1.08
    cool_d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    cool_b = np.exp(-((cool_d / (0.55 * w)) ** 2))
    dither = 1.0 + 0.01 * np.sin(xx * 0.29 + yy * 0.17)
    bloom = bloom * dither
    cool_b = cool_b * dither

    warm = hex_rgb("#F0C49A")
    gold = hex_rgb("#E8D7B0")
    cool = hex_rgb("#9AABAA")
    mix_w = (bloom * 0.22)[..., None]
    mix_g = (bloom * 0.10)[..., None]
    mix_c = (cool_b * 0.07)[..., None]
    img = img * (1.0 - mix_w) + warm * mix_w
    img = img * (1.0 - mix_g) + gold * mix_g
    img = img * (1.0 - mix_c) + cool * mix_c
    return np.clip(img, 0.0, 1.0)


def pad_frame(img: np.ndarray, inset: int, color: np.ndarray, alpha: float, width: int = 2) -> np.ndarray:
    """Quiet outer frame, typical of an engineering pad. Stays in the margin."""
    h, w, _ = img.shape
    layer = np.zeros((h, w, 3), dtype=np.float32)
    a = np.zeros((h, w), dtype=np.float32)
    x0, y0 = inset, inset
    x1, y1 = w - inset, h - inset
    if x1 - x0 < 8 or y1 - y0 < 8:
        return img
    layer[...] = color
    a[y0 : y0 + width, x0:x1] = alpha
    a[y1 - width : y1, x0:x1] = alpha
    a[y0:y1, x0 : x0 + width] = alpha
    a[y0:y1, x1 - width : x1] = alpha
    return np.clip(img * (1.0 - a[..., None]) + layer * a[..., None], 0.0, 1.0)


# ---------------------------------------------------------------------------
# variants
# ---------------------------------------------------------------------------

def render(variant: str, w: int, h: int) -> Image.Image:
    cell = w // CELL_DIV
    # Deterministic per variant and size, so re-runs match.
    seed = {"A": 20261119, "B": 20261121, "C": 20261123}[variant] + w + h
    rng = np.random.default_rng(seed)
    ew = edge_weight(h, w, softness=max(80.0, w * 0.07))

    if variant == "A":
        base = hex_rgb("#F4EFE3")
        img = paper_body(
            h, w, rng,
            base=base,
            mottle_amp=0.007,
            mottle_tint=hex_rgb("#E8D9B8"),
            grain_amp=0.015,
            fiber_amp=0.008,
            fleck_density=0.00012,
            fleck_color=hex_rgb("#C9B394"),
        )
        # Barely-there top lighting, warmer toward the lower edge.
        yy, _ = mesh(h, w)
        lift = (1.0 - yy / h)
        img = np.clip(img * (0.985 + 0.025 * lift[..., None]), 0.0, 1.0)

        img = apply_grid(
            img, cell,
            minor_rgb=hex_rgb("#A9C4D8"), minor_a=0.28,
            major_rgb=hex_rgb("#87A9C4"), major_a=0.40,
            major_width=2 if cell >= 24 else 1,
        )
        # Red margin on a grid line, well inside the left margin.
        margin_x = cell * 4
        img = apply_margin_line(img, margin_x, hex_rgb("#C45A5A"), alpha=0.38, width=2)

        rgb, a = coffee_ring(
            h, w,
            cx=w * 0.09, cy=h * 0.86,
            radius=min(w, h) * 0.085,
            rng=rng,
            color=hex_rgb("#8B5A32"),
            strength=0.30,
        )
        img = composite(img, rgb, a, ew)

        rgb, a = tape_piece(
            h, w,
            cx=w * 0.86, cy=h * 0.055,
            tw=w * 0.16, th=h * 0.055,
            angle_deg=-8.5,
            color=hex_rgb("#E6D4A4"),
            rng=rng,
            opacity=0.50,
        )
        img = composite_tape(img, rgb, a, ew)

        # A second, smaller tape tab at the lower-right, just peeking in.
        rgb, a = tape_piece(
            h, w,
            cx=w * 0.97, cy=h * 0.78,
            tw=w * 0.07, th=h * 0.09,
            angle_deg=12.0,
            color=hex_rgb("#E2C98E"),
            rng=rng,
            opacity=0.44,
        )
        img = composite_tape(img, rgb, a, ew)

        img = binding_and_wear(
            img, rng,
            shadow_rgb=hex_rgb("#C9B79A"),
            yellow_rgb=hex_rgb("#D9C29A"),
            shadow_amp=0.10,
            yellow_amp=0.10,
            left_bind=True,
        )

    elif variant == "B":
        base = hex_rgb("#0B1424")
        img = paper_body(
            h, w, rng,
            base=base,
            mottle_amp=0.010,
            mottle_tint=hex_rgb("#152A40"),
            grain_amp=0.016,
            fiber_amp=0.007,
            fleck_density=0.00008,
            fleck_color=hex_rgb("#1C3348"),
        )
        img = apply_grid(
            img, cell,
            minor_rgb=hex_rgb("#3E8A9A"), minor_a=0.16,
            major_rgb=hex_rgb("#5AAFC0"), major_a=0.26,
            major_width=2 if cell >= 24 else 1,
        )
        margin_x = cell * 4
        img = apply_margin_line(img, margin_x, hex_rgb("#4E9AA8"), alpha=0.22, width=2)

        img = lamp_glow(h, w, img)

        # A barely-visible mug ring in the lower left — the late-night companion.
        rgb, a = coffee_ring(
            h, w,
            cx=w * 0.10, cy=h * 0.88,
            radius=min(w, h) * 0.07,
            rng=rng,
            color=hex_rgb("#120806"),
            strength=0.40,
        )
        img = composite(img, rgb, a, ew)

        img = binding_and_wear(
            img, rng,
            shadow_rgb=hex_rgb("#050810"),
            yellow_rgb=hex_rgb("#152033"),
            shadow_amp=0.22,
            yellow_amp=0.10,
            left_bind=True,
        )

    elif variant == "C":
        base = hex_rgb("#C6D0BC")
        img = paper_body(
            h, w, rng,
            base=base,
            mottle_amp=0.007,
            mottle_tint=hex_rgb("#B7C4A8"),
            grain_amp=0.014,
            fiber_amp=0.007,
            fleck_density=0.00010,
            fleck_color=hex_rgb("#9AA88C"),
        )
        img = dawn_wash(h, w, img)
        img = apply_grid(
            img, cell,
            minor_rgb=hex_rgb("#7E9278"), minor_a=0.30,
            major_rgb=hex_rgb("#667A62"), major_a=0.44,
            major_width=2 if cell >= 24 else 1,
        )
        # Engineering pads often carry a printed frame in the margin.
        img = pad_frame(
            img,
            inset=max(18, cell),
            color=hex_rgb("#5E7258"),
            alpha=0.28,
            width=2,
        )
        # Soft pencil-ish smudge, lower left, well out of the well.
        rgb, a = coffee_ring(
            h, w,
            cx=w * 0.07, cy=h * 0.90,
            radius=min(w, h) * 0.055,
            rng=rng,
            color=hex_rgb("#6A5A40"),
            strength=0.16,
        )
        img = composite(img, rgb, a, ew)

        rgb, a = tape_piece(
            h, w,
            cx=w * 0.14, cy=h * 0.035,
            tw=w * 0.13, th=h * 0.048,
            angle_deg=6.0,
            color=hex_rgb("#D9CBA0"),
            rng=rng,
            opacity=0.42,
        )
        img = composite_tape(img, rgb, a, ew)

        img = binding_and_wear(
            img, rng,
            shadow_rgb=hex_rgb("#9AA490"),
            yellow_rgb=hex_rgb("#C4B08A"),
            shadow_amp=0.09,
            yellow_amp=0.08,
            left_bind=True,
        )
    else:
        raise ValueError(f"unknown variant {variant}")

    rgb8 = to_uint8_dither(img, rng)
    return Image.fromarray(rgb8, mode="RGB")


# ---------------------------------------------------------------------------
# contact sheet + CLI
# ---------------------------------------------------------------------------

def _font(size: int):
    for path in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ):
        p = Path(path)
        if p.exists():
            return ImageFont.truetype(str(p), size=size)
    return ImageFont.load_default()


def make_contact(images: dict[tuple[str, int, int], Image.Image], path: Path) -> None:
    """3 columns (A B C) × 2 rows (1920 / 1280), labeled for review only."""
    order = ["A", "B", "C"]
    titles = {
        "A": "A  warm off-white",
        "B": "B  night shift",
        "C": "C  engineering pad / dawn",
    }
    thumb_w = 640
    gap = 24
    label_h = 36
    header_h = 72
    footer_h = 28
    thumbs: list[list[Image.Image]] = []
    row_heights: list[int] = []
    for (tw, th) in SIZES:
        row = []
        thumb_h = int(round(thumb_w * th / tw))
        row_heights.append(thumb_h)
        for v in order:
            im = images[(v, tw, th)].resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            row.append(im)
        thumbs.append(row)

    sheet_w = gap + len(order) * (thumb_w + gap)
    sheet_h = header_h + sum(h + label_h + gap for h in row_heights) + footer_h
    sheet = Image.new("RGB", (sheet_w, sheet_h), (32, 32, 34))
    draw = ImageDraw.Draw(sheet)
    font_h = _font(22)
    font_s = _font(15)
    font_t = _font(13)
    draw.text((gap, 18), "pstack-jissen  ·  lab-notebook backgrounds (text-free)", font=font_h, fill=(236, 236, 232))
    draw.text((gap, 46), "Central ~60% is kept clear for screenshots, banners and video title cards.", font=font_s, fill=(160, 160, 158))

    y = header_h
    for r, (tw, th) in enumerate(SIZES):
        for c, v in enumerate(order):
            x = gap + c * (thumb_w + gap)
            sheet.paste(thumbs[r][c], (x, y))
            # Hairline around each thumb so the paper edge is visible on the dark board.
            draw.rectangle([x, y, x + thumb_w - 1, y + row_heights[r] - 1], outline=(70, 70, 72))
            caption = f"{titles[v]}    {tw}×{th}"
            draw.text((x, y + row_heights[r] + 8), caption, font=font_t, fill=(200, 200, 196))
        y += row_heights[r] + label_h + gap

    path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(path, format="JPEG", quality=92, subsampling=0, optimize=True)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    images: dict[tuple[str, int, int], Image.Image] = {}
    for variant in ("A", "B", "C"):
        for w, h in SIZES:
            print(f"rendering {variant} {w}x{h} ...", flush=True)
            im = render(variant, w, h)
            images[(variant, w, h)] = im
            dest = OUT / f"bg_{variant}_{w}x{h}.png"
            im.save(dest, format="PNG", optimize=True)
            print(f"  wrote {dest}  ({dest.stat().st_size / 1024:.0f} KB)")

    contact = OUT / "bg_contact.jpg"
    make_contact(images, contact)
    print(f"wrote {contact}  ({contact.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
