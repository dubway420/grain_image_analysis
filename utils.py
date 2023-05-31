import os
from grain_size_analysis import grain_list
from openpyxl import Workbook

def path_validation(input_folder_path, image_ext):

    # Check if input_folder_path is absolute
    if not os.path.isabs(input_folder_path):
        input_folder_path = os.path.join(os.getcwd(), input_folder_path) # If not, add the current working directory to it

    # Check if specified input folder exists
    if os.path.isdir(input_folder_path):
       
       # Check if specified input folder contains .csv files
       if not any(fname.endswith(image_ext) for fname in os.listdir(input_folder_path)):
           print(f"Warning: the path to the folder of inputs ({input_folder_path}) does not contain {image_ext} files. Please check and try again.")
           return False

    else:
        print(f"Warning: the path to the folder of inputs ({input_folder_path}) does not exist. Please check and try again.") 
        return False

    return input_folder_path      

def multiple_grain_analysis(input_folder_path="Inputs", output_folder_path="Outputs", image_ext=".png", pix_len=891, sca_len=200):

    # Validate the input and output parameter
    input_folder = path_validation(input_folder_path, image_ext)
    
    grains = []

    # If valid, continue
    if input_folder:

        # Iterate through the files in the input folder
        for file in os.listdir(input_folder):
            
            # If it ends with the image extension, continue
            if file.endswith(image_ext):

                file_fullpath = os.path.join(input_folder, file)
                grains.append((file, grain_list(file_fullpath, pix_len, sca_len)))

        return grains

