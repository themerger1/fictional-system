#just drag and drop file or folder to convert
#import sys
from pathlib import Path
from PIL import Image


def convert_png_to_jpg(input_file, output_folder):
    try:
        img = Image.open(input_file)

        # Handle PNG transparency
        if img.mode in ("RGBA", "LA") or "transparency" in img.info:
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img = background
        else:
            img = img.convert("RGB")

        output_path = output_folder / (input_file.stem + ".jpg")

        img.save(output_path, "JPEG", quality=95)

        print(f"Converted: {input_file.name}")

    except Exception as e:
        print(f"Failed: {input_file} ({e})")


def process_folder(folder):
    folder = Path(folder)

    # Create output folder inside source folder
    output_folder = folder / folder.name
    output_folder.mkdir(exist_ok=True)

    png_files = list(folder.glob("*.png"))

    if not png_files:
        print(f"No PNG found in: {folder}")
        return

    for png in png_files:
        convert_png_to_jpg(png, output_folder)


def process_input(path):
    path = Path(path)

    if path.is_file():
        if path.suffix.lower() == ".png":
            convert_png_to_jpg(path, path.parent)
        else:
            print(f"Skip (not PNG): {path}")

    elif path.is_dir():
        process_folder(path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Drag PNG files or folders onto this script.")
        input("Press Enter to exit...")
    else:
        for item in sys.argv[1:]:
            process_input(item)

    input("\nDone. Press Enter to exit...")
