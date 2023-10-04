# Import the modules
import os
import zipfile
import shutil
import sys
import glob
import re
import natsort


# A function to convert degrees, minutes, seconds (DMS) to decimal degrees (DD)
def dms_to_dd(degrees, minutes, seconds, direction):
    dd = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'S' or direction == 'W':
        dd *= -1
    return dd

# A function to parse a GPGGA message and return an array with [lat, lon, alt]


def parse_gpgga(message):
    # Split the message by comma
    fields = message.split(b",")
    # Check if the message is valid
    if message.find(b"$GPGGA") != -1 and fields[6] != '0':
        # Extract the latitude, longitude and altitude
        lat_deg = fields[2][:2]
        lat_min = fields[2][2:4]
        lat_sec = fields[2][5:]
        lat_dir = fields[3]
        lon_deg = fields[4][:3]
        lon_min = fields[4][3:5]
        lon_sec = fields[4][6:]
        lon_dir = fields[5]
        alt = fields[9]
        # Convert the latitude and longitude from DMS to DD
        lat = round(dms_to_dd(lat_deg, lat_min, lat_sec, lat_dir), 8)
        lon = round(dms_to_dd(lon_deg, lon_min, lon_sec, lon_dir), 8)
        # encode the latitude and longitude as bytes
        lat = bytes(str(lat), 'utf-8')
        lon = bytes(str(lon), 'utf-8')
        # Return an array with [lat, lon, alt]
        return [lat, lon, alt]
    else:
        # Return an empty array if the message is invalid
        return []


# Define a function to process a single file


def process_file(file_path, output_file):
    # Open the file in binary mode
    time_date_valid = False
    lat_lon_alt_valid = False
    with open(file_path, "rb") as f:
        # Skip the first two lines
        f.readline()
        f.readline()
        # Read the rest of the file and write to the output file
        for line in f:
            fields = line.split(b",")

            # if the line has a GPRMC string, write it to the output file
            if line.find(b"$GPRMC") != -1:
                time_date = [fields[9], fields[1]]
                if time_date is not None:
                    time_date_valid = True

            if line.find(b"$GPGGA") != -1:
                lat_lon_alt = parse_gpgga(line)
                if lat_lon_alt is not None:
                    lat_lon_alt_valid = True

            # if the line is valid, write it to the output file
            if line.strip() and time_date_valid and lat_lon_alt_valid and not line.startswith(b"PPS") and not any(c in b"$#@%^&*!" for c in line) and not re.match(b"[a-zA-Z]", line):
                # remove the newline character from the last field of original line
                fields[-1] = fields[11].strip()
                # add the date and time to the end of the line
                fields.extend(time_date)
                # add the latitude, longitude and altitude to the end of the line
                fields.extend(lat_lon_alt)
                # add a newline character to the end of the line
                fields[-1] += b"\r\n"
                line = b",".join(fields)
                output_file.write(line)

# Define a function to process a zip file or a regular folder


def process_zip_or_folder(input_path, output_path):
    # Create the output file name based on the input path
    output_file_name = os.path.basename(input_path).split(".")[
        0] + "_merged_data.txt"
    # Open the output file in binary mode
    with open(os.path.join(output_path, output_file_name), "wb") as output_file:
        # Check if the input path is a zip file or a regular folder
        if input_path.endswith(".zip"):
            # Open the zip file
            with zipfile.ZipFile(input_path, "r") as z:
                # Get the list of files in the zip file and sort them by natural order (1, 2, 3, ...)
                files = z.namelist()
                files = natsort.natsorted(files)
                # Get the number of files to process (excluding acquinfo.txt)
                num_files = len(files) - \
                    1 if "acquinfo.txt" in files else len(files)
                # Print the number of files to process
                print(f"\nProcessing {num_files} files from {input_path}...")
                # Loop through the sorted files in the zip file
                for i, name in enumerate(files, start=1):
                    # Skip the acquinfo.txt file
                    if name == "acquinfo.txt":
                        continue
                    # Extract the file to a temporary folder
                    z.extract(name, "temp")
                    # Print the current file name and number
                    print(f"Processing file {i} of {num_files}: {name}")
                    # Process the file
                    process_file(os.path.join("temp", name),
                                 output_file)
            # Remove the temporary folder
            shutil.rmtree("temp")
        else:
            # Get the list of files in the regular folder and sort them by natural order (1, 2, 3, ...)
            files = os.listdir(input_path)
            files = natsort.natsorted(files)
            # Get the number of files to process (excluding acquinfo.txt)
            num_files = len(files) - \
                1 if "acquinfo.txt" in files else len(files)
            # Print the number of files to process
            print(f"\nProcessing {num_files} files from {input_path}...")
            # Loop through the sorted files in the regular folder
            for i, name in enumerate(files, start=1):
                # Skip the acquinfo.txt file
                if name == "acquinfo.txt":
                    continue
                # Print the current file name and number
                print(f"Processing file {i} of {num_files}: {name}")
                # Process the file
                process_file(os.path.join(input_path, name),
                             output_file)


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
    # Find all files in ./raw_data that start with ACQU and process them
    for folder in glob.glob(os.path.join(input_path, "ACQU*")):
        process_zip_or_folder(folder, output_path)
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
