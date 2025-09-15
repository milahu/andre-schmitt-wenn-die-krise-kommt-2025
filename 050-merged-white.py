#!/usr/bin/env python3

r"""
chatGPT prompt:

create a python script to merge images.
process all images from an input directory.
write output files to a separate output directory.

some input images have multiple parts:
0336-00100.png
0336-00200.png
0336-00300.png
merge these 3 parts into the output image 0336.png

"merge" means: create a vertical stack from the input images

some input images have only one part
this part's filename always ends with "-00100.png"
in this case, copy the input image
and only remove the filename suffix "-00100.png"



If an input group has multiple parts: merge vertically.

If an input group has a single part: instead of just copying,
pair it with the next available single-part group,
and merge those two single-part images vertically into one output image.
only consecutive single-part images should be merged.

If there’s an odd leftover single-part image (no partner), just copy it as before.
"""

import os
import re
from PIL import Image

INPUT_DIR = "white"
OUTPUT_DIR = "050-merged-white"

# Regex to match filenames like 0336-00100.png
pattern = re.compile(r"^(\d{4})-\d{5}\.png$")

def merge_images_vertically(images, out_path):
    widths = [img.width for img in images]
    heights = [img.height for img in images]

    max_width = max(widths)
    total_height = sum(heights)

    merged = Image.new("RGB", (max_width, total_height), (255, 255, 255))

    y_offset = 0
    for img in images:
        merged.paste(img, (0, y_offset))
        y_offset += img.height

    merged.save(out_path)


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Group images by base prefix (before the dash)
    groups = {}
    for fname in sorted(os.listdir(INPUT_DIR)):
        if pattern.match(fname):
            base = fname.split("-")[0]
            groups.setdefault(base, []).append(fname)

    single_part_bases = []

    for base, files in groups.items():
        files.sort()  # ensure order by suffix number

        if len(files) == 1:
            single_part_bases.append(base)
        else:
            # Multiple parts: merge vertically
            images = [Image.open(os.path.join(INPUT_DIR, f)) for f in files]
            out_name = base + ".png"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            merge_images_vertically(images, out_path)
            print(f"Merged {len(files)} parts -> {out_name}")

    # Sort single-part bases numerically
    single_part_bases = sorted(single_part_bases, key=lambda x: int(x))

    i = 0
    while i < len(single_part_bases):
        base1 = single_part_bases[i]
        f1 = groups[base1][0]
        img1 = Image.open(os.path.join(INPUT_DIR, f1))

        if i + 1 < len(single_part_bases):
            base2 = single_part_bases[i + 1]
            # Check if consecutive numbers
            if int(base2) == int(base1) + 1:
                f2 = groups[base2][0]
                img2 = Image.open(os.path.join(INPUT_DIR, f2))

                out_name = f"{base1}_{base2}.png"
                out_path = os.path.join(OUTPUT_DIR, out_name)
                merge_images_vertically([img1, img2], out_path)
                print(f"Merged consecutive singles {f1} + {f2} -> {out_name}")
                i += 2
                continue

        # No consecutive match → save single
        out_name = base1 + ".png"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        img1.save(out_path)
        print(f"Copied single {f1} -> {out_name}")
        i += 1

if __name__ == "__main__":
    main()
