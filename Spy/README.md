<<<<<<< HEAD
# System Monitor (Spy) Application

A comprehensive system monitoring application built with PyQt6 that provides keylogging, webcam capture, screenshot functionality, and Chrome password extraction capabilities.

## Features

1. **Keylogger**: Records all keyboard inputs with timestamps
2. **Webcam Capture**: Takes photos from the webcam at configurable intervals
3. **Screenshot Capture**: Takes screen captures at configurable intervals
4. **Chrome Password Extraction**: Extracts saved passwords from Chrome browser
5. **Configuration Dialog**: Customize monitoring settings
6. **Multi-threaded Operation**: All monitoring runs in separate threads
7. **Progress Tracking**: Real-time progress updates and status

## Requirements

- Python 3.7 or higher
- Windows OS (for Chrome password extraction)

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Usage

### Main Interface
- **Start**: Begin monitoring with current configuration
- **Show Data**: View captured data (keylog, webcam photos, screenshots, passwords)
- **Configure**: Open configuration dialog to customize settings
- **Stop**: Stop current monitoring session
- **Close**: Exit the application

### Configuration Options

#### Keylogger Settings
- Enable/disable keylogger
- Press ESC to stop keylogger manually

#### Webcam Settings
- Enable/disable webcam capture
- Set number of photos to capture
- Set interval between photos (seconds)

#### Screenshot Settings
- Enable/disable screenshot capture
- Set number of screenshots to capture
- Set interval between screenshots (seconds)

#### Password Extraction
- Enable/disable Chrome password extraction
- Requires Chrome browser and appropriate permissions

## File Structure

```
project_GUI/Spy/
├── main.py              # Main application file
├── keylogger.py         # Auto-generated UI file
├── keylogger.ui         # UI design file
├── requirements.txt     # Dependencies
├── README.md           # This file
├── key/                # Keylogger output
│   └── key.txt
├── webcam/             # Webcam captures
├── screen_shot/        # Screenshots
└── web_passwd/         # Chrome passwords
    └── passwd.txt
```

## Data Output

- **Keylogger**: Stored in `key/key.txt` with timestamps
- **Webcam Photos**: Stored in `webcam/` folder with timestamps
- **Screenshots**: Stored in `screen_shot/` folder with timestamps
- **Chrome Passwords**: Stored in `web_passwd/passwd.txt`

## Security Notes

⚠️ **Important**: This application is designed for educational and legitimate monitoring purposes only. Users are responsible for:

1. Complying with local laws and regulations
2. Obtaining proper consent before monitoring
3. Securing captured data appropriately
4. Using the application ethically and responsibly

## Troubleshooting

### Common Issues

1. **Screenshot not working**: 
   - Ensure pyautogui is installed: `pip install pyautogui`
   - Check if the application has screen capture permissions

2. **Webcam not working**:
   - Ensure opencv-python is installed
   - Check if camera is available and not used by another application

3. **Password extraction not working**:
   - Ensure Chrome is closed during extraction
   - Requires Windows OS and proper permissions
   - Install pycryptodome and pywin32

4. **Keylogger not working**:
   - May require administrator privileges
   - Ensure pynput is installed correctly

### Dependencies Issues

If you encounter import errors, reinstall all dependencies:
```bash
pip uninstall -y pyautogui opencv-python pynput pycryptodome pywin32 PyQt6 pillow
pip install -r requirements.txt
```

## Technical Details

- Built with PyQt6 for the GUI
- Uses threading for concurrent monitoring
- Implements proper error handling and fallback methods
- Supports graceful shutdown and cleanup
- Progress tracking with real-time updates

## License

This project is for educational purposes. Please ensure you comply with all applicable laws and regulations when using this software.
=======
# Project_GUI_Python
Graphic projects in Python
>>>>>>> 1900b56c5a481be31b1ae92edac8bad91fd48d97
