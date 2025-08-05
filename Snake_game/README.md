# Snake Game 🐍

A classic Snake game implementation built with Python and Tkinter GUI library.

## Description

This is a traditional Snake game where the player controls a snake to collect food while avoiding collisions with walls and the snake's own body. The game features a simple and intuitive interface with score tracking and restart functionality.

## Features

- **Classic Gameplay**: Control the snake using arrow keys
- **Score System**: Track your score as you collect food
- **Collision Detection**: Game ends when snake hits walls or itself
- **Restart Function**: Easy restart button to play again
- **Centered Window**: Game window automatically centers on screen
- **Smooth Movement**: Configurable snake speed

## Game Controls

- **Arrow Keys**: Control snake direction
  - ⬆️ Up Arrow: Move up
  - ⬇️ Down Arrow: Move down
  - ⬅️ Left Arrow: Move left
  - ➡️ Right Arrow: Move right
- **Restart Button**: Click to restart the game

## Game Configuration

The game includes several customizable parameters:

- **Game Area**: 700x700 pixels
- **Grid Size**: 20x20 pixels per tile
- **Initial Snake Length**: 2 segments
- **Snake Speed**: 200ms delay between moves
- **Colors**:
  - Snake: Yellow
  - Food: Red
  - Background: Black

## Installation

### Prerequisites

- Python 3.6 or higher
- tkinter (usually comes pre-installed with Python)

### Setup

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   # or download the ZIP file and extract it
   ```

2. **Navigate to the project directory**:
   ```bash
   cd Snake_game
   ```

3. **Install dependencies** (if needed):
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the game by executing the main Python file:

```bash
python main.py
```

### How to Play

1. **Start the Game**: Run `main.py` to open the game window
2. **Control the Snake**: Use arrow keys to change the snake's direction
3. **Collect Food**: Move the snake to the red circular food items
4. **Avoid Collisions**: Don't hit the walls or the snake's own body
5. **Track Your Score**: Your score increases each time you eat food
6. **Restart**: Click the "Restart" button to start a new game

## Game Rules

- The snake moves continuously in the current direction
- Eating food increases your score by 1 point
- The snake grows longer each time it eats food
- Game ends if the snake:
  - Hits any wall (boundaries)
  - Collides with its own body
- Use the restart button to play again

## File Structure

```
Snake_game/
├── main.py          # Main game file
├── README.md        # This file
└── requirements.txt # Python dependencies
```

## Code Structure

The game is organized into several key components:

- **Snake Class**: Manages snake body, movement, and rendering
- **Food Class**: Handles food generation and positioning
- **Game Loop**: Controls game flow and timing
- **Event Handlers**: Processes keyboard input
- **Collision Detection**: Checks for game-ending conditions

## Customization

You can easily modify the game by changing the constants at the top of `main.py`:

```python
GAME_WIDTH = 700        # Game window width
GAME_HEIGHT = 700       # Game window height
SPACE_SIZE = 20         # Size of each grid tile
BODY_SIZE = 2           # Initial snake length
SLOWNESS = 200          # Snake speed (lower = faster)
SNAKE_COLOR = 'yellow'  # Snake color
FOOD_COLOR = 'red'      # Food color
BACKGROUND_COLOR = 'black'  # Background color
```

## Troubleshooting

### Common Issues

1. **tkinter not found**: Install tkinter using your system package manager
   - Ubuntu/Debian: `sudo apt-get install python3-tk`
   - macOS: tkinter comes with Python
   - Windows: tkinter comes with Python

2. **Game window not appearing**: Make sure you're running Python 3.6+

3. **Performance issues**: Try increasing the SLOWNESS value for slower gameplay

## Contributing

Feel free to contribute to this project by:

- Adding new features (sound effects, high score system, etc.)
- Improving the user interface
- Optimizing the code
- Fixing bugs
- Adding more customization options

## License

This project is open source and available under the [MIT License](LICENSE).

## Acknowledgments

- Built with Python's built-in tkinter library
- Inspired by the classic Snake arcade game
- Persian comments in original code maintained for reference

---

**Enjoy playing the Snake Game!** 🎮
