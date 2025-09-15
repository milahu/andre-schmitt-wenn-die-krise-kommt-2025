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

INPUT_DIR = "040-level-images"
OUTPUT_DIR = "050-merged-white"

# Regex to match filenames like 0336-00100.png
pattern = re.compile(r"^(\d+)-\d{5}\.png$")

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

    # Iterate over a static list of keys to avoid RuntimeError
    for base in list(groups.keys()):
        files = groups[base]
        files.sort()  # ensure order by suffix number
        n = len(files)

        if n == 1:
            single_part_bases.append(base)
        elif n == 2:
            # Merge 2 parts
            images = [Image.open(os.path.join(INPUT_DIR, f)) for f in files]
            out_name = base + ".png"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            merge_images_vertically(images, out_path)
            print(f"Merged 2 parts {files} -> {out_name}")
        elif n == 3:
            # Merge first 2 parts
            images = [Image.open(os.path.join(INPUT_DIR, files[0])), Image.open(os.path.join(INPUT_DIR, files[1]))]
            out_name = base + ".png"
            out_path = os.path.join(OUTPUT_DIR, out_name)
            merge_images_vertically(images, out_path)
            print(f"Merged first 2 parts of 3 {files[:2]} -> {out_name}")

            # Treat 3rd part as single-part image
            new_base = base + '_part3'
            groups[new_base] = [files[2]]
            single_part_bases.append(new_base)

    # Sort single-part bases numerically (ignore '_part3' suffix for sorting)
    def sort_key(b):
        return int(re.match(r'(\d+)', b).group(1))

    single_part_bases = sorted(single_part_bases, key=sort_key)

    # Merge consecutive single-part images
    i = 0
    while i < len(single_part_bases):
        base1 = single_part_bases[i]
        f1 = groups[base1][0]
        img1 = Image.open(os.path.join(INPUT_DIR, f1))

        if i + 1 < len(single_part_bases):
            base2 = single_part_bases[i + 1]
            # Check if consecutive numbers
            num1 = int(re.match(r'(\d+)', base1).group(1))
            num2 = int(re.match(r'(\d+)', base2).group(1))
            if num2 == num1 + 1:
                f2 = groups[base2][0]
                img2 = Image.open(os.path.join(INPUT_DIR, f2))
                # out_name = f"{num1}_{num2}.png"
                out_name = f"{num1:04d}_{num2:04d}.png"
                out_path = os.path.join(OUTPUT_DIR, out_name)
                merge_images_vertically([img1, img2], out_path)
                print(f"Merged consecutive singles {f1} + {f2} -> {out_name}")
                i += 2
                continue

        # No consecutive match → save single
        out_name = re.match(r'(\d+)', base1).group(1) + ".png"
        out_path = os.path.join(OUTPUT_DIR, out_name)
        img1.save(out_path)
        print(f"Copied single {f1} -> {out_name}")
        i += 1

if __name__ == "__main__":
    main()
