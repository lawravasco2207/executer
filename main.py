from flask import Flask
import os
import datetime

app = Flask(__name__)

BASE_DIRECTORY = "/storage/emulated/0/DCIM"  # Change this if needed

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}  # Supported image types

def find_image_directory(base_dir):
    """Find the first directory containing images inside the base directory."""
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in IMAGE_EXTENSIONS):
                return root  # Return the first directory found with images
    return None  # No image directory found

def delete_images_last_7_days():
    """Find the image directory and delete images modified in the last 7 days."""
    image_dir = find_image_directory(BASE_DIRECTORY)
    if not image_dir:
        return "No image directory found."

    current_date = datetime.datetime.now()
    seven_days_ago = current_date - datetime.timedelta(days=7)

    # Collect images modified within the last 7 days
    files_to_delete = [
        os.path.join(image_dir, filename)
        for filename in os.listdir(image_dir)
        if os.path.isfile(os.path.join(image_dir, filename)) and
        any(filename.lower().endswith(ext) for ext in IMAGE_EXTENSIONS) and
        seven_days_ago <= datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(image_dir, filename))) <= current_date
    ]

    # Delete images in batch
    if files_to_delete:
        try:
            for file_path in files_to_delete:
                os.remove(file_path)
            return f"Deleted {len(files_to_delete)} images from the last 7 days in {image_dir}."
        except Exception as e:
            return f"Error deleting files: {e}"
    
    return "No images deleted."

@app.route('/')
def index():
    return "Welcome to the Image Cleanup Service. Click <a href='/delete_images'>here</a> to delete images from the last 7 days."

@app.route('/delete_images')
def delete_images():
    result = delete_images_last_7_days()
    return f"{result} <br><a href='/'>Go back</a>."

if __name__ == '__main__':
    app.run(debug=True)
