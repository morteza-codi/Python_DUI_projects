# File Manager

A desktop application for managing files and directories with a graphical user interface built using PyQt6.

## Features

- **Open Files**: Open files with their default application
- **Copy Files**: Copy files from one location to another
- **Delete Files**: Delete files with confirmation
- **Rename Files**: Rename files while preserving their extension
- **Move Files**: Move files from one location to another with overwrite confirmation
- **Create Directories**: Create new directories
- **Remove Directories**: Remove empty directories or directories with contents (with confirmation)
- **List Files**: View files and directories in a selected folder with size information

## Screenshots

*Screenshots can be added here*

## Requirements

- Python 3.6+
- PyQt6
- OS: Windows, macOS, or Linux

## Installation

1. Clone this repository or download the source code:
```
git clone https://github.com/yourusername/file_manager.git
cd file_manager
```

2. Install the required dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python main.py
```

## Usage

1. Launch the application by running `main.py`
2. Use the buttons on the left panel to perform various file operations:
   - **open_file**: Opens a file with its default application
   - **copy_file**: Copies a file to another location
   - **delete_file**: Deletes a file (with confirmation)
   - **rename_file**: Renames a file
   - **move_file**: Moves a file to another location
   - **make_directory**: Creates a new directory
   - **remove_directory**: Removes a directory
   - **list_files**: Lists files in a directory
   - **close**: Closes the application

## Project Structure

- `main.py`: Main application code
- `file.py`: UI definition generated from the Qt Designer file
- `file.ui`: Qt Designer UI file

## License

*Add your license information here*

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- PyQt6 for providing the GUI framework
- Qt Designer for the UI design tool 