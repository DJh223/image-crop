# image-crop

Crop images to 16:9 aspect ratio from the command line.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Crop an image to 16:9 (default: center anchor)
python crop_16_9.py photo.jpg

# Specify output path
python crop_16_9.py photo.jpg -o cropped.jpg

# Choose crop position
python crop_16_9.py photo.jpg -p top
python crop_16_9.py photo.jpg -p bottom
python crop_16_9.py photo.jpg -p left
python crop_16_9.py photo.jpg -p right

# Adjust JPEG quality
python crop_16_9.py photo.jpg -q 85
```

The script crops from the center by default. For images wider than 16:9, it trims the sides. For images taller than 16:9, it trims the top and bottom.

## Web UI

Open [`web/index.html`](web/index.html) in your browser for a visual drag-and-drop interface.

Features:
- Drag & drop image upload
- Free-drag crop box locked to 16:9 — drag to move, corner handles to resize
- Rule-of-thirds grid guides
- Real-time preview
- Download cropped result
- Dark mode / touch support
