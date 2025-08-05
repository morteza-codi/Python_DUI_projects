# Coin Collecting Game

A simple and fun coin collecting game built with Python and Pygame. Avoid obstacles while collecting coins to increase your score!

## Game Description

This is an arcade-style game where you control a player character that moves horizontally at the bottom of the screen. Your objective is to:
- 🪙 **Collect yellow coins** to increase your score (+10 points each)
- 🚫 **Avoid red obstacles** that fall from the top of the screen
- 🎯 **Survive as long as possible** as the game gets progressively faster

## Features

- **Simple Controls**: Use left and right arrow keys to move
- **Progressive Difficulty**: Both obstacles and coins fall faster as you play
- **Score System**: Earn 10 points for each coin collected
- **Game Over Screen**: Shows your final score and restart option
- **Dark Mode**: Clean dark theme for comfortable gameplay
- **Persian Title**: The game window displays "بازی سکه و مانع" (Coin and Obstacle Game)

## Screenshots

The game features:
- Gray player rectangle at the bottom
- Red rectangular obstacles falling from the top
- Yellow circular coins to collect
- Score display in the top-left corner
- Game over screen with restart option

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

If you don't have a requirements.txt file, install Pygame manually:

```bash
pip install pygame
```

## How to Run

1. Navigate to the project directory
2. Run the game:

```bash
python main.py
```

## Controls

- **Left Arrow Key**: Move player left
- **Right Arrow Key**: Move player right
- **Enter**: Restart game after game over

## Gameplay Rules

1. **Movement**: Your player (gray rectangle) can move left and right at the bottom of the screen
2. **Obstacles**: Red rectangular obstacles fall from the top - avoid them!
3. **Coins**: Yellow circular coins fall from the top - collect them for points
4. **Collision**: Touching an obstacle ends the game
5. **Scoring**: Each coin collected gives you 10 points
6. **Speed**: The game gets progressively faster as you play

## Game Over

When you hit an obstacle:
- The game displays "Game Over"
- Your final score is shown
- Press Enter to restart and play again

## Technical Details

- **Resolution**: 800x800 pixels
- **Frame Rate**: 60 FPS
- **Language**: Python 3
- **Graphics Library**: Pygame
- **Platform**: Cross-platform (Windows, macOS, Linux)

## File Structure

```
Coin_collecting_game/
│
├── main.py           # Main game file
├── README.md         # This file
├── requirements.txt  # Python dependencies
└── .idea/           # IDE configuration files
```

## Development

The game is built using:
- **Python**: Core programming language
- **Pygame**: Graphics and game development library
- **Random**: For generating random positions for obstacles and coins

### Key Game Variables

- Player speed: 10 pixels per frame
- Initial obstacle speed: 3 pixels per frame
- Initial coin speed: 4 pixels per frame
- Speed increase: 0.2 pixels per frame (progressive difficulty)
- Score per coin: 10 points

## Future Enhancements

Potential improvements for the game:
- Add sound effects and background music
- Include different types of coins with varying point values
- Add power-ups (speed boost, invincibility, etc.)
- Implement a high score system
- Add different obstacle types and patterns
- Include particle effects for coin collection
- Add pause functionality
- Implement different difficulty levels

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for any improvements!

---

Enjoy playing the Coin Collecting Game! 🎮🪙
