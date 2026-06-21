from __future__ import annotations

import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps


def parse_example_name(path: Path) -> str:
    name = path.stem

    match = re.search(r"class_examples_\d+_(.+?)_to_(.+)$", name)
    if match:
        true_class = match.group(1)
        pred_class = match.group(2)
        status = "Correct" if true_class == pred_class else "Wrong"
        return f"{status}: {true_class} -> {pred_class}"

    match = re.search(r"high_confidence_failure_\d+_(.+?)_to_(.+)$", name)
    if match:
        true_class = match.group(1)
        pred_class = match.group(2)
        return f"Failure: {true_class} -> {pred_class}"

    return name


def discover_gradcam_images(input_dir: Path, max_images: int) -> list[Path]:
    patterns = [
        "*class_examples*.png",
        "*high_confidence_failure*.png",
        "*gradcam*.png",
    ]

    files: list[Path] = []
    for pattern in patterns:
        files.extend(sorted(input_dir.glob(pattern)))

    unique_files = []
    seen = set()

    for file in files:
        if file.name in seen:
            continue
        if file.name == "gradcam_summary.png":
            continue
        seen.add(file.name)
        unique_files.append(file)

    return unique_files[:max_images]


def make_thumbnail(image_path: Path, size: tuple[int, int], title: str) -> Image.Image:
    image = Image.open(image_path).convert("RGB")
    image = ImageOps.contain(image, size)

    canvas_width, canvas_height = size
    title_height = 42

    canvas = Image.new("RGB", (canvas_width, canvas_height + title_height), "white")

    x = (canvas_width - image.width) // 2
    y = title_height
    canvas.paste(image, (x, y))

    draw = ImageDraw.Draw(canvas)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except Exception:
        font = ImageFont.load_default()

    draw.text((10, 10), title[:95], fill="black", font=font)

    return canvas


def build_summary(
    image_paths: list[Path],
    output_path: Path,
    columns: int,
    thumbnail_width: int,
    thumbnail_height: int,
) -> None:
    if not image_paths:
        raise RuntimeError("No Grad-CAM images found.")

    thumbnails = [
        make_thumbnail(
            image_path=path,
            size=(thumbnail_width, thumbnail_height),
            title=parse_example_name(path),
        )
        for path in image_paths
    ]

    rows = (len(thumbnails) + columns - 1) // columns

    cell_width = thumbnail_width
    cell_height = thumbnail_height + 42

    canvas = Image.new(
        "RGB",
        (columns * cell_width, rows * cell_height),
        "white",
    )

    for idx, thumbnail in enumerate(thumbnails):
        row = idx // columns
        col = idx % columns
        canvas.paste(thumbnail, (col * cell_width, row * cell_height))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a single Grad-CAM summary image from existing Grad-CAM PNG files."
    )

    parser.add_argument(
        "--input-dir",
        default="reports/figures/gradcam",
        help="Directory containing Grad-CAM PNG files.",
    )

    parser.add_argument(
        "--output",
        default="reports/figures/gradcam/gradcam_summary.png",
        help="Output summary PNG path.",
    )

    parser.add_argument(
        "--max-images",
        type=int,
        default=6,
        help="Maximum number of Grad-CAM images to include.",
    )

    parser.add_argument(
        "--columns",
        type=int,
        default=1,
        help="Number of columns in the summary grid.",
    )

    parser.add_argument(
        "--thumbnail-width",
        type=int,
        default=1800,
        help="Thumbnail canvas width.",
    )

    parser.add_argument(
        "--thumbnail-height",
        type=int,
        default=620,
        help="Thumbnail image height.",
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = Path(args.output)

    image_paths = discover_gradcam_images(
        input_dir=input_dir,
        max_images=args.max_images,
    )

    print(f"Found {len(image_paths)} Grad-CAM images.")
    for path in image_paths:
        print(f"- {path}")

    build_summary(
        image_paths=image_paths,
        output_path=output_path,
        columns=args.columns,
        thumbnail_width=args.thumbnail_width,
        thumbnail_height=args.thumbnail_height,
    )

    print(f"Saved Grad-CAM summary to: {output_path}")


if __name__ == "__main__":
    main()