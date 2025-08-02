# Spy Tool

A monitoring application built with Python and PyQt6 that captures keystrokes, screenshots, webcam images, and browser passwords.

## Features

- **Keylogger**: Records keyboard input and saves it to a text file
- **Screenshot Capture**: Takes periodic screenshots of the screen
- **Webcam Capture**: Takes periodic images from the webcam
- **Browser Password Extraction**: Extracts saved passwords from Chrome browser
- **Data Viewer**: View all captured data in a user-friendly interface
- **Configurable Settings**: Customize capture intervals and counts

## Requirements

- Windows OS
- Python 3.8+
- Chrome browser (for password extraction)
- Webcam (for webcam capture)

## Installation

1. Clone the repository or download the source code
2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

1. Run the application:

```
python main.py
```

2. Click the "START" button to begin monitoring
3. Click the "SHOW DATA" button to view captured data
4. Click the "SETTINGS" button to configure capture settings
5. Click the "EXIT" button to close the application

## Configuration

You can configure the following settings:

- Number of webcam captures
- Interval between webcam captures (in seconds)
- Number of screenshot captures
- Interval between screenshot captures (in seconds)

Settings are saved to `spy_config.json` in the application directory.

## Data Storage

Data is stored in the following directories:

- Keystrokes: `./key/key.txt`
- Webcam images: `./webcam/`
- Screenshots: `./screen_shot/`
- Browser passwords: `./web_passwd/passwd.txt`

## Disclaimer

This tool is intended for educational purposes only. Using this tool to monitor others without their knowledge or consent may be illegal in your jurisdiction. Always obtain proper authorization before using this tool.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
