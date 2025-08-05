# Coin Collecting Game
بازی سکه و مانع

A simple 2D arcade-style game built with Pygame where players collect coins while avoiding falling obstacles.

## Features

- **Player Movement**: Control a gray square using arrow keys
- **Coin Collection**: Collect yellow coins to increase your score
- **Obstacle Avoidance**: Dodge red rectangular obstacles falling from the top
- **Progressive Difficulty**: Game speed increases as you play
- **Score System**: Earn 10 points for each coin collected
- **Game Over & Restart**: Press Enter after game over to play again
- **Dark Mode Interface**: Clean dark theme for better visibility

## How to Play

1. **Movement**: Use the LEFT and RIGHT arrow keys to move your player
2. **Objective**: Collect as many yellow coins as possible while avoiding red obstacles
3. **Scoring**: Each coin gives you 10 points
4. **Game Over**: The game ends when you hit a red obstacle
5. **Restart**: Press Enter after game over to start a new game

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or Download** this repository to your local machine

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Game**:
   ```bash
   python main.py
   ```

## Game Controls

| Key | Action |
|-----|--------|
| ← (Left Arrow) | Move player left |
| → (Right Arrow) | Move player right |
| Enter | Restart game (after game over) |
| X (Close Window) | Quit game |

## Game Mechanics

- **Player**: Gray rectangle that moves horizontally at the bottom of the screen
- **Coins**: Yellow circles that fall from the top at random positions
- **Obstacles**: Red rectangles that fall from the top at random positions
- **Speed Increase**: Both coins and obstacles gradually increase in speed
- **Collision Detection**: Game ends when player touches any obstacle
- **Coin Collection**: Player earns points by touching coins

## Technical Details

- **Resolution**: 800x800 pixels
- **Frame Rate**: 60 FPS
- **Built With**: Python + Pygame
- **Platform**: Cross-platform (Windows, macOS, Linux)

## Game Statistics

- **Player Size**: 50x50 pixels
- **Obstacle Size**: 150x20 pixels
- **Coin Radius**: 15 pixels
- **Initial Speed**: 
  - Obstacles: 3 pixels/frame
  - Coins: 4 pixels/frame
- **Speed Increase**: 0.2 pixels/frame per cycle

## Screenshots

The game features:
- Dark background for better contrast
- Simple geometric shapes for retro arcade feel
- Real-time score display
- Clean game over screen with restart option

## Development

This is a beginner-friendly Pygame project demonstrating:
- Basic game loop implementation
- Collision detection
- Random object generation
- Score tracking and display
- Game state management (playing/game over)

## Future Enhancements

Potential improvements could include:
- Power-ups and special coins
- Multiple lives system
- High score persistence
- Sound effects and background music
- Different obstacle types
- Difficulty levels

## License

This project is open source and available under standard terms.

## Support

If you encounter any issues or have questions about the game, please check that you have:
1. Python 3.6+ installed
2. Pygame properly installed via pip
3. All game files in the same directory

Enjoy playing the Coin Collecting Game! 🪙
