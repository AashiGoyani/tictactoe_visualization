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

## Application Flow

### Game Flow
1. **Initialize Game**: User clicks "New Game" → Flask creates new TicTacToeGame instance
2. **Human Move**: User clicks cell → Frontend sends move to `/make_move` endpoint
3. **Move Validation**: Backend validates move and updates game state
4. **AI Decision**: Game engine calculates move values using trained Q-values
5. **AI Move**: AI selects best move and updates board
6. **Game Tree Generation**: Backend generates decision tree for visualization
7. **Response**: Frontend receives updated board state and move analysis
8. **Visualization**: Tree visualization panel shows AI's decision process

### Data Flow
```
Frontend (HTML/JS) ↔ Flask API ↔ Game Engine ↔ AI Agent (Q-values)
                                       ↓
                               Game Tree Generator
```

### Key Components Interaction
- **Flask App**: Handles HTTP requests and game state management
- **TicTacToeGame**: Core game logic and move validation
- **AI Agent**: Uses temporal difference learning with pre-trained values
- **Game Tree**: Visualizes possible moves and their evaluations

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

You can also specify the number of training episodes:
```bash
python train_agent.py --episodes 50000
```

This will generate new Q-values and save them to `trained_agent_values.pkl`.
