import os
from PIL import Image

def repair_jpeg(input_path, output_folder, reference_path):
    # Open the input image
    with Image.open(input_path) as img:
        # Remove exif and thumbnail
        img.info.clear()
        # Find the last ffda+12bytes
        marker = b"\xff\xda"
        with open(input_path, "rb") as f:
            data = f.read()
        idx = data.rfind(marker) + len(marker)
        # Take from soi to ffda+12bytes ( 1 )
        repaired_data = data[:idx]
        # Take from offset 153605 to end of file and remove 334 bytes from end of file ( 2 )
        repaired_data += data[153605:-334]
    
    # Open the reference image
    with Image.open(reference_path) as ref:
        # Copy the EXIF data from the reference image to the repaired image
        img.info["exif"] = ref.info["exif"]
    
    # Create the output folder path
    output_folder_path = os.path.join(output_folder, "Repaired")
    # Check if the output folder exists, if not create it
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    # Save the repaired image to the output folder
    output_name = os.path.splitext(os.path.basename(input_path))[0] + ".jpg"
    output_path = os.path.join(output_folder_path, output_name)
    with open(output_path, "wb") as f:
        f.write(repaired_data)
        

def batch_repair_jpeg():
    # Ask the user for the corrupt JPEG folder path
    input_folder = input("Enter the path to the corrupt JPEG folder: ")
    
    # Check if the input folder exists
    if not os.path.exists(input_folder):
        print("Error: The specified folder does not exist.")
        return
    
    # Ask the user for the reference JPEG file path
    reference_path = input("Enter the path to the reference JPEG file: ")
    
    # Check if the reference file exists
    if not os.path.exists(reference_path):
        print("Error: The specified file does not exist.")
        return
    
    # Loop through all JPEG files in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.lower().endswith(".jpg"):
            # Add the corrupt folder path to the file name
            input_path = os.path.join(input_folder, file_name)
            # Repair the JPEG file and save it to the output folder
            repair_jpeg(input_path, input_folder, reference_path)
