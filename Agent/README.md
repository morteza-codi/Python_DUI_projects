# AI Assistant

This project is a voice-activated AI Assistant developed using Python and PyQt6. It allows users to perform various tasks using voice commands, such as searching Wikipedia, opening YouTube, checking the time, taking photos, making calculations, and more.

## Features

- **Voice Commands**: Interact with the assistant using natural language.
- **Graphical User Interface**: Built with PyQt6 for easy interaction.
- **Text-to-Speech**: Converts text responses to speech using pyttsx3.
- **Speech Recognition**: Processes voice input through the microphone.
- **Web Integration**: Interacts with web services like Google, Wikipedia, YouTube.
- **Local Features**: Includes tasks like taking photos, checking the system time, setting reminders, etc.

## Installation

1. **Clone the repository**: Make sure you have Git installed and run:
   ```bash
   git clone <repository-url>
   cd path/to/your/project
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

## Configuration
- **Settings**: User-specific settings are stored in `assistant_settings.json`.
- **Speech Recognition**: Requires `PyAudio` for microphone access.

## Usage

- **Start the Assistant**: Run the main.py script.
- **Voice Commands**: Activate the assistant via commands like "open YouTube", "what's the weather", "take a photo", etc.
- **User Interface**: You can interact using the buttons provided for different functionalities like Text to Speech, Speech to Text, and VIP options.

## License

This project is open source and available under the MIT License.

---

Ensure that the appropriate API keys and configurations are setup in the code where necessary, such as Wolfram Alpha and OpenWeatherMap.
