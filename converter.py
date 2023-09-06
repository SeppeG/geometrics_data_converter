# Import the modules
import os
import zipfile
import shutil
import sys
import glob
import re
import natsort

# Define a function to process a single file


def process_file(file_path, output_file):
    # Open the file in binary mode
    with open(file_path, "rb") as f:
        # Skip the first two lines
        f.readline()
        f.readline()
        # Read the rest of the file and write to the output file
        for line in f:
            # Skip empty lines, lines that start with PPS, lines that have a special character, or lines that start with a letter
            if line.strip() and not line.startswith(b"PPS") and not any(c in b"$#@%^&*!" for c in line) and not re.match(b"[a-zA-Z]", line):
                output_file.write(line)

# Define a function to process a zip file or a regular folder


def process_zip_or_folder(input_path, output_path):
    # Create the output file name based on the input path
    output_file_name = os.path.basename(input_path).split(".")[0] + "_data.txt"
    # Open the output file in binary mode
    with open(os.path.join(output_path, output_file_name), "wb") as output_file:
        # Check if the input path is a zip file or a regular folder
        if input_path.endswith(".zip"):
            # Open the zip file
            with zipfile.ZipFile(input_path, "r") as z:
                # Get the list of files in the zip file and sort them by natural order (1, 2, 3, ...)
                files = z.namelist()
                files = natsort.natsorted(files)
                # Get the number of files to process (excluding aquinfo.txt)
                num_files = len(files) - \
                    1 if "aquinfo.txt" in files else len(files)
                # Print the number of files to process
                print(f"Processing {num_files} files from {input_path}...")
                # Loop through the sorted files in the zip file
                for i, name in enumerate(files, start=1):
                    # Skip the aquinfo.txt file
                    if name == "aquinfo.txt":
                        continue
                    # Extract the file to a temporary folder
                    z.extract(name, "temp")
                    # Print the current file name and number
                    print(f"Processing file {i} of {num_files}: {name}")
                    # Process the file
                    process_file(os.path.join("temp", name), output_file)
            # Copy the aquinfo.txt file to the output folder if it exists
            aquinfo_path = os.path.join("temp", "aquinfo.txt")
            if os.path.exists(aquinfo_path):
                shutil.copy(aquinfo_path, output_path)
            # Remove the temporary folder
            shutil.rmtree("temp")
        else:
            # Get the list of files in the regular folder and sort them by natural order (1, 2, 3, ...)
            files = os.listdir(input_path)
            files = natsort.natsorted(files)
            # Get the number of files to process (excluding aquinfo.txt)
            num_files = len(files) - \
                1 if "aquinfo.txt" in files else len(files)
            # Print the number of files to process
            print(f"Processing {num_files} files from {input_path}...")
            # Loop through the sorted files in the regular folder
            for i, name in enumerate(files, start=1):
                # Skip the aquinfo.txt file
                if name == "aquinfo.txt":
                    continue
                # Print the current file name and number
                print(f"Processing file {i} of {num_files}: {name}")
                # Process the file
                process_file(os.path.join(input_path, name), output_file)
            # Copy the aquinfo.txt file to the output folder if it exists
            aquinfo_path = os.path.join(input_path, "aquinfo.txt")
            if os.path.exists(aquinfo_path):
                shutil.copy(aquinfo_path, output_path)


# Get the number of arguments passed to the script
num_args = len(sys.argv)

# Check if no arguments are passed
if num_args == 1:
    # Set the default input and output paths as relative paths
    input_path = "./raw_data"
    output_path = "./output"
    # Create the output folder if it does not exist
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # Find all zip files in ./data that start with ACQU and process them
    for zip_file in glob.glob(os.path.join(input_path, "ACQU*.zip")):
        process_zip_or_folder(zip_file, output_path)
# Check if two arguments are passed (input and output paths)
elif num_args == 3:
    # Get the input and output paths from the arguments as relative paths
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    # Check if the input path is valid
    if not os.path.exists(input_path):
        print("Invalid input path. Please try again.")
        sys.exit(1)
    # Create the output folder if it does not exist
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # Process the input path
    process_zip_or_folder(input_path, output_path)
# Otherwise, print an error message and exit
else:
    print("Invalid number of arguments. Please provide either no arguments or two arguments (input and output paths).")
    sys.exit(1)
