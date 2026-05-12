from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps


MAX_SIZE = (750, 350)
INPUT_DIR = Path("images")
OUTPUT_DIR = INPUT_DIR / "formatted"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def main() -> None:
    if not INPUT_DIR.is_dir():
        print(f"Images folder not found: {INPUT_DIR.resolve()}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    processed = 0
    for image_path in sorted(INPUT_DIR.iterdir()):
        if not image_path.is_file() or image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            formatted = format_image(image_path)
        except OSError as error:
            print(f"Skipped {image_path.name}: {error}")
            continue

        output_path = OUTPUT_DIR / f"{image_path.stem}.png"
        formatted.save(output_path, "PNG", optimize=True)

        processed += 1
        print(f"Done: {image_path.name} -> {output_path} ({formatted.width}x{formatted.height})")

    print(f"Processed images: {processed}")


def format_image(image_path: Path) -> Image.Image:
    with Image.open(image_path) as image:
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")
        image.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        image = image.copy()

    if image_path.stem.lower() == "manager":
        return enhance_manager_image(image)

    return image

def enhance_manager_image(image: Image.Image) -> Image.Image:
    image = ImageEnhance.Color(image).enhance(1.16)
    image = ImageEnhance.Contrast(image).enhance(1.08)
    image = ImageEnhance.Brightness(image).enhance(1.04)
    return image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=3))


if __name__ == "__main__":
    main()
