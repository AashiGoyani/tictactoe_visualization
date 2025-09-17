from flask import Flask, render_template, request, jsonify
import json
from copy import deepcopy
from game_engine import TicTacToeGame, Agent

app = Flask(__name__)

games = {}
last_decision_context = {}  # Store the decision context for tree visualization

@app.route('/')
def index():
    return render_template('split_view.html')

@app.route('/td_vis')
def td_visualization():
    return render_template('td_vis.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    game = TicTacToeGame()
    game_id = id(game)
    games[game_id] = game
    
    return jsonify({
        'board': game.board,
        'status': 'active',
        'current_player': 'human',
        'game_id': game_id
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    row = data['row']
    col = data['col']
    game_id = data.get('game_id')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 400
    
    game = games[game_id]
    
    if not game.is_valid_move(row, col):
        return jsonify({'error': 'Invalid move'}), 400
    
    game.make_move(row, col, 1)
    winner = game.check_winner()
    
    if winner:
        return jsonify({
            'board': game.board,
            'status': 'finished',
            'winner': 'human' if winner == 1 else 'draw' if winner == 3 else 'ai'
        })
    
    # Get move values BEFORE AI makes its move (for left panel display)
    move_values = game.get_move_values()
    
    # Store the decision context for tree visualization
    last_decision_context[game_id] = {
        'board': deepcopy(game.board),
        'move_values': move_values.copy()
    }
    
    ai_move = game.ai_move()
    
    # Now make the AI move
    if ai_move:
        game.make_move(ai_move[0], ai_move[1], 2)
        winner = game.check_winner()
    
    return jsonify({
        'board': game.board,
        'status': 'finished' if winner else 'active',
        'winner': 'ai' if winner == 2 else 'draw' if winner == 3 else None,
        'ai_move': ai_move,
        'move_values': move_values
    })

@app.route('/game_tree', methods=['POST'])
def get_game_tree():
    data = request.get_json()
    game_id = data.get('game_id')
    depth = data.get('depth', 2)
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 400
    
    # Check if we have stored decision context (board state before AI move)
    if game_id in last_decision_context:
        # Use the board state from when AI was making its decision
        decision_context = last_decision_context[game_id]
        temp_game = TicTacToeGame()
        temp_game.board = decision_context['board']
        temp_game.ai_agent.values = games[game_id].ai_agent.values  # Use same trained values
        tree = temp_game.generate_game_tree()
        source = 'decision_context'
    else:
        # Fallback to current game state
        game = games[game_id]
        tree = game.generate_game_tree()
        source = 'current_state'
    
    return jsonify({
        'tree': tree,
        'current_board': games[game_id].board,
        'source': source
    })



if __name__ == '__main__':
    app.run(debug=True, port=5001)