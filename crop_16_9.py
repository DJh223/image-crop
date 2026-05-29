#!/usr/bin/env python3
"""Crop images to 16:9 aspect ratio."""

import argparse
import sys
from pathlib import Path

from PIL import Image


def crop_to_16_9(
    image: Image.Image,
    position: str = "center",
) -> Image.Image:
    """Crop an image to 16:9 aspect ratio.

    Args:
        image: PIL Image to crop.
        position: Where to anchor the crop - "center", "top", or "bottom".

    Returns:
        Cropped PIL Image.
    """
    target_ratio = 16 / 9
    width, height = image.size
    current_ratio = width / height

    if abs(current_ratio - target_ratio) < 0.001:
        return image

    if current_ratio > target_ratio:
        # Image is wider than 16:9 - crop width
        new_width = int(height * target_ratio)
        if position == "center":
            left = (width - new_width) // 2
        elif position == "left":
            left = 0
        elif position == "right":
            left = width - new_width
        else:
            raise ValueError(f"Unknown position: {position}")
        return image.crop((left, 0, left + new_width, height))
    else:
        # Image is taller than 16:9 - crop height
        new_height = int(width / target_ratio)
        if position == "center":
            top = (height - new_height) // 2
        elif position == "top":
            top = 0
        elif position == "bottom":
            top = height - new_height
        else:
            raise ValueError(f"Unknown position: {position}")
        return image.crop((0, top, width, top + new_height))


def main():
    parser = argparse.ArgumentParser(
        description="Crop images to 16:9 aspect ratio."
    )
    parser.add_argument(
        "input",
        type=Path,
        help="Path to the input image.",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        help="Path for the output image. Defaults to <input>_16_9.<ext>.",
    )
    parser.add_argument(
        "-p", "--position",
        choices=["center", "top", "bottom", "left", "right"],
        default="center",
        help="Crop anchor position (default: center). "
             "For horizontal crops: left/center/right. "
             "For vertical crops: top/center/bottom.",
    )
    parser.add_argument(
        "-q", "--quality",
        type=int,
        default=95,
        help="JPEG output quality (default: 95).",
    )
    parser.add_argument(
        "--format",
        help="Output format (jpg, png, webp). Auto-detected from output extension.",
    )

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    if args.output is None:
        stem = args.input.stem
        suffix = args.input.suffix or ".jpg"
        args.output = args.input.parent / f"{stem}_16_9{suffix}"

    try:
        with Image.open(args.input) as img:
            cropped = crop_to_16_9(img, args.position)
            save_kwargs = {}
            if (args.format or args.output.suffix).lower() in (".jpg", ".jpeg"):
                save_kwargs["quality"] = args.quality
                save_kwargs["optimize"] = True
            cropped.save(args.output, **save_kwargs)

        print(f"Saved: {args.output}")
        print(f"Size: {cropped.size[0]}x{cropped.size[1]}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
