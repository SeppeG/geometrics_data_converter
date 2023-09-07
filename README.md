# geometrics_data_converter

> Convert Acquisition data from the Geometrics MFAM Development Kit to a single txt file

This is a python script that reads a zip file or a regular folder containing multiple files named 1.txt 2.txt 3.txt … (charset=binary) and one file named aquinfo.txt and merges the files starting with a number into one big txt file, on each separate file, the first 2 lines need to be removed, as well as any empty lines, in the end you should have a new folder named <folder_name> containing one txt file named <folder_name>_data.txt and one file aquinfo.txt. The output txt file is also in binary txt.

## Requirements

- Python 3
- zipfile module
- shutil module
- sys module
- glob module
- re module
- natsort module

## Usage

You can run the script from the command line with the following syntax:

`python3 converter.py <input path> <output path>`

The input path can be either a zip file or a regular folder. The output path must be a folder. If you do not provide any arguments, the script will use the default input path as ./data and the output path as ./output. It will also convert all zip files in ./data that start with ACQU.

## Example

Suppose you have a zip file named ACQU_2023_01.zip in the raw_data directory. It contains the following files:

- 1.txt
- 2.txt
- 3.txt
- aquinfo.txt

You want to merge the files 1.txt, 2.txt and 3.txt into one big txt file named ACQU_2023_01_data.txt. You can run the script as follows:

`python3 converter.py`

The script will merge the files and save it in the output folder as ACQU_2023_01_data.txt.

The ACQU_2023_01_data.txt file will be a binary txt file that contains the merged content of 1.txt, 2.txt and 3.txt without the first two lines and any empty lines.

## Message definition

| Field | Structure | Field Description                                               | Symbol    |   |
|-------|-----------|-----------------------------------------------------------------|-----------|---|
| 1     | ID        | Tezzeret global millisecond counter                             |           |   |
| 2     | Fiducial  | Increments with every magnetometer sample                       |           |   |
| 3     | FrameID   | The fiducial number is a subset of the FrameID value            |           |   |
| 4     | SysStat   | The two upper bits of this 16-bit word indicate GPS 1PPS status |           |   |
| 5     | Mag1D     | Sensor 1 measurement.                                           |           |   |
| 6     | Mag1S     | Sensor 1 status                                                 |           |   |
| 7     | Mag2D     | Sensor 2 measurement                                            |           |   |
| 8     | Mag2S     | Sensor 2 status                                                 |           |   |
| 9     | Aux0      |                                                                 |           |   |
| 10    | Aux1      |                                                                 |           |   |
| 11    | Aux2      |                                                                 |           |   |
| 12    | Aux3      |                                                                 |           |   |
| 13    | Date      | Date: dd/mm/yy (1Hz)                                            | xxxxxx    |   |
| 14    | UTC       | UTC of position (1Hz)                                           | hhmmss.ss |   |
| 15    | lat       | Latitude (decimal degrees) (1Hz)                                | x.x       |   |
| 17    | lon       | Longitude (decimal degrees) (1Hz)                               | x.x       |   |
| 18    | alt       | Antenna altitude above/below mean sea level (1Hz)               | x.x       |   |
