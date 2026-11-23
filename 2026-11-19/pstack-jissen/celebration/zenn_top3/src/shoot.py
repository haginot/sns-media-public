"""Prepare the Tech section and article crops from the supplied logged-out captures."""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def redact_bylines(section, boxes):
    background = section.getpixel((0, 0))
    draw = ImageDraw.Draw(section)
    for box in boxes:
        draw.rectangle(box, fill=background)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("full", type=Path)
    parser.add_argument("card", type=Path)
    args = parser.parse_args()

    with Image.open(args.full) as full:
        section = full.convert("RGB").crop((245, 320, 1185, 690))
    redact_bylines(section, [(140, 169, 451, 209), (605, 165, 781, 209),
                            (140, 316, 451, 360), (605, 315, 850, 360)])
    section.save("shot_tech_section_raw.png")
    section.crop((17, 12, 930, 362)).save("shot_top3.png")

    with Image.open(args.card) as card:
        article = card.convert("RGB").crop((31, 229, 463, 357))
    redact_bylines(article, [(115, 88, 431, 127)])
    article.save("shot_row.png")
