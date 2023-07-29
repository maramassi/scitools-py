# scitools-py
Python script to extract metrics from Scitools (Understand tool) (https://scitools.com/) using Python

# Clone Genealogy Analysis Script

## Description
This Python script is designed to analyze clone genealogies and generate Understand project databases (`udb` files) for specific commits of a project. The script leverages the `git` version control system, `Understand` tool, and various Python libraries to perform the following tasks:

1. Extract commit hashes from a sequence file for the given project.
2. Analyze clone snapshots from XML files to extract unique file paths for each commit.
3. Build Understand project databases for each commit, containing clone-related metrics.
4. Check out the repository at each commit, perform necessary analysis, and generate `udb` files.

## Dependencies
The script relies on the following Python libraries, which you must have installed before running it:
- `logging`: Provides logging functionality for debugging and monitoring.
- `subprocess`: Allows running shell commands from Python.
- `sys`: Provides access to Python interpreter and system-related information.
- `os`: Allows interaction with the operating system (e.g., file paths, directory changes).
- `time`: Enables time-related operations like sleeping.
- `platform`: Retrieves system information such as Python version.
- `tqdm`: A library for creating progress bars during iteration.
- `pandas`: Used for handling data as DataFrames.
- `shutil`: Offers file and directory manipulation capabilities.
- `config_py`: A custom configuration file containing global settings for the project.
- `xml.etree.ElementTree`: Library for parsing and analyzing XML data.
- `understand`: The Understand Python API for working with `udb` files.

## Execution
To use this script, follow these steps:

1. Ensure you have the required dependencies installed.
2. Modify the `config_global.py` file to set global configuration settings, such as file paths and settings for Understand analysis.
3. Make sure your Python environment can access the `Understand` tool from the command line or update the `sys.path.append()` lines in the script to point to the correct path.
4. Prepare the necessary data:
   - Create a sequence file (`project_sequence_all.txt`) containing commit hashes for the project.
   - Organize clone results in XML files (one file per commit) with `<source>` tags specifying file paths.

5. Run the script from the command line, providing the name of the project as an argument:
   python script_name.py project_name
