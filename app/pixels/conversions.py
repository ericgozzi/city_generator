from PIL import Image
import os


def convert_images_to_png(input_folder, output_folder):
    """
    Converts all images in the specified folder to PNG format and saves them in the output folder.
    
    Args: 
        param input_folder (str): Path to the folder containing the images.
        param output_folder (str): Path to the folder where PNG images will be saved.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        if os.path.isfile(input_path):
            try:
                with Image.open(input_path) as img:
                    output_filename = os.path.splitext(filename)[0] + ".png"
                    output_path = os.path.join(output_folder, output_filename)
                    img.save(output_path, "PNG")
                    print(f"Converted: {filename} -> {output_filename}")
            except Exception as e:
                print(f"Failed to convert {filename}: {e}")