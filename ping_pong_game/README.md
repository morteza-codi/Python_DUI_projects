# Ping Pong Game 🎮

Enjoy a classic Ping Pong game built with Python and Pygame!

## Overview

This Ping Pong game is a two-player game where players use paddles to hit a ball back and forth across the screen. The game is played to 5 points, and the first player to score 5 points wins.

## Features

- **Two-Player Mode**: Control paddles using keyboard.
- **Score Tracking**: Display player scores on the screen.
- **Collision Detection**: Ball bounces off paddles and walls.
- **Restart Game**: Game resets when a player wins.
- **Customizable**: Adjustable speeds for ball and paddles.

## Controls

- **Player 1**: 
  - `W`: Move paddle up
  - `S`: Move paddle down
- **Player 2**:
  - `UP Arrow`: Move paddle up
  - `DOWN Arrow`: Move paddle down
- **Space Bar**: Start the ball movement

## Installation

### Prerequisites

- Python 3.6 or higher
- Pygame library

### Setup

1. Clone or download the project:
   ```bash
   git clone <repository-url>
   # or download the ZIP file and extract it
   ```

2. Navigate to the project directory:
   ```bash
   cd ping_pong_game
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Game

Run the following command to start the game:
```bash
python main.py
```

## Game Rules

- The ball moves continuously once started.
- Players score points by getting the ball past the opponent's paddle.
- The game ends when a player scores 5 points.

## Configuration Options

You can customize the game settings in `main.py`:

- **Ball Speed**: Change `BALL_SPEED` value for difficulty.
- **Paddle Speed**: Change `PADDLE_SPEED` value.
- **Player Names**: Modify `player1_name` and `player2_name` in the code.

## Troubleshooting

### Common Issues

1. **Pygame not found**: Make sure Pygame is installed using `pip install pygame`.
2. **Lag or Performance Issues**: Adjust game speed settings for smoother gameplay.

## Contributing

Feel free to contribute with new features, improvements, or bug fixes.

## Acknowledgments

- Built using the powerful [Pygame](https://www.pygame.org/wiki/about) library.
- A simple implementation inspired by the classic pong game.

Enjoy the game! 🏓
