# Tic-Tac-Toe with AI

A web-based Tic-Tac-Toe game featuring an AI opponent with temporal difference learning and game tree visualization.

## Features

- **Interactive Web Interface**: Play Tic-Tac-Toe against an AI opponent through a clean web interface
- **AI Agent**: Trained using temporal difference learning with stored Q-values
- **Game Tree Visualization**: View the AI's decision-making process through game tree exploration
- **Split View**: Simultaneous gameplay and AI analysis visualization

## Files

- `app.py` - Flask web application with game API endpoints
- `game_engine.py` - Core game logic and AI agent implementation
- `train_agent.py` - Script for training the AI agent
- `trained_agent_values.pkl` - Pre-trained AI agent Q-values
- `templates/` - HTML templates for the web interface
- `static/` - CSS and JavaScript assets

## Setup

1. Install dependencies:
   ```bash
   pip install flask
   ```

2. Run the application:
   ```bash
   python app.py
   ```

3. Open your browser to `http://localhost:5001`

## How to Play

1. Click "New Game" to start
2. Click on any empty cell to make your move
3. The AI will automatically respond
4. View the AI's decision process in the tree visualization panel

## AI Training

To retrain the AI agent, run:
```bash
python train_agent.py
```

This will generate new Q-values and save them to `trained_agent_values.pkl`.# tictactoe_visualization
