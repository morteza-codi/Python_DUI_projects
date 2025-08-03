# Lottery Drawing Application

A simple and fair lottery drawing application built with PyQt6 that randomly selects winners from a list of participants.

## Features

- **Random Winner Selection**: Randomly selects a specified number of winners from a list of participants
- **File-based Input**: Load participants from a text file (one name per line)
- **Configurable Winner Count**: Choose how many winners to select
- **Winner Display**: Shows the list of winners in a separate dialog
- **Copy to Clipboard**: Easily copy the winners list to clipboard
- **User-friendly GUI**: Built with PyQt6 for a modern, native look

## Requirements

- Python 3.8 or higher
- PyQt6

## Installation

1. Clone or download this repository to your local machine.

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python main.py
   ```

2. **Select Participants File**:
   - Click the "choice file" button
   - Browse and select a text file containing participant names (one name per line)

3. **Set Number of Winners**:
   - Enter the number of winners you want to select in the "count" field

4. **Draw Winners**:
   - Click "Selection of winners" to randomly select the winners
   - A dialog will appear showing the selected winners

5. **Copy Winners**:
   - In the winners dialog, click "Copy" to copy the list to your clipboard

## File Format

The participants file should be a plain text file with one participant name per line:

```
John Doe
Jane Smith
Bob Johnson
Alice Williams
...
```

Empty lines will be ignored.

## Project Structure

```
lottery/
├── main.py           # Main application logic and entry point
├── lottery.py        # PyQt6 UI code (generated from untitled.ui)
├── untitled.ui       # Qt Designer UI file
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Error Handling

The application includes error handling for common issues:
- Empty or missing participant files
- Invalid number of winners (negative or non-integer values)
- Requesting more winners than available participants
- File reading errors

## Development

The UI was designed using Qt Designer and converted to Python code using PyQt6's `pyuic6` tool. If you modify the UI file, regenerate the Python code:

```bash
pyuic6 untitled.ui -o lottery.py
```

## License

This project is open source. Feel free to use and modify it as needed.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.
