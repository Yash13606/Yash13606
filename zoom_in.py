import sys
from PIL import Image

def zoom_image(input_path, output_path, zoom_factor=1.5):
    img = Image.open(input_path)
    w, h = img.size
    
    new_w, new_h = int(w / zoom_factor), int(h / zoom_factor)
    
    left = (w - new_w) / 2
    top = (h - new_h) / 2
    right = (w + new_w) / 2
    bottom = (h + new_h) / 2
    
    img = img.crop((left, top, right, bottom))
    img.save(output_path)
    print(f"Cropped {input_path} by {zoom_factor}x to {output_path}")

if __name__ == "__main__":
    zoom_image(sys.argv[1], sys.argv[2], float(sys.argv[3]))
