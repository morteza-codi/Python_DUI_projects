# Snake Game

A classic Snake game built with Python and Tkinter. Navigate your snake, grow by eating red food, and avoid crashing into yourself or the boundaries!

## Game Description

This Snake game allows you to control the snake's direction using arrow keys to:
- 🍎 **Eat red food** to grow longer
- 🚫 **Avoid running into the walls or yourself**
- 🎯 **Try to achieve the highest score possible**

## Features

- **Simple Controls**: Use arrow keys to change the snake's direction
- **Score System**: Increases as your snake eats more food
- **Game Over Screen**: Displays when you hit the wall or yourself
- **Restart Option**: Restart the game at any time

## Screenshots

### Main Features
- Moving yellow snake squares
- Red food target
- Black screen background
- Dynamic score display
- Centered game window

## Installation

### Prerequisites

Make sure you have Python 3.6 or higher installed on your system.

### Install Dependencies

1. Clone or download this project
2. Navigate to the project directory
3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Alternative Installation

If you don't have a requirements.txt file, install Tkinter manually:

- For Windows and macOS, `tkinter` is included with Python
- For Linux, use your package manager (e.g., `sudo apt-get install python3-tk`)

## How to Run

1. Navigate to the project directory
2. Run the game:

```bash
python main.py
```

## Controls

- **Left Arrow Key**: Move snake left
- **Right Arrow Key**: Move snake right
- **Up Arrow Key**: Move snake up
- **Down Arrow Key**: Move snake down

## Gameplay Rules

1. **Movement**: Change the snake's direction using arrow keys
2. **Growth**: Eating food increases the snake's length and score
3. **Collision**: Crashing into walls or yourself ends the game

## Game Over

When the snake collides:
- The game displays "GAME OVER!"
- Press the restart button to play again

## Technical Details

- **Resolution**: 700x700 pixels
- **Frame Rate**: Handled by Tkinter's event loop
- **Language**: Python 3
- **GUI Library**: Tkinter
- **Platform**: Cross-platform (Windows, macOS, Linux)

## File Structure

```
Snake_game/
│
├── main.py           # Main game file
├── README.md         # This file
├── requirements.txt  # Python dependencies
└── .idea/           # IDE configuration files
```

## Development

The game involves:
- **Python**: Core programming language
- **Tkinter**: For GUI development
- **Random**: For generating random positions for food

### Key Game Variables

- Snake speed and space size
- Initial direction is downward
- Food and snake color settings

## Future Enhancements

Potential improvements for the game:
- Add sound effects
- Implement different difficulty levels
- Add high score tracking
- Include power-ups (speed boost, invincibility, etc.)
- Different levels or themes
- Online score leaderboard

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

---

Enjoy playing the classic Snake Game! 🐍🍏
