import random
from copy import deepcopy

EMPTY = 0
PLAYER_X = 1
PLAYER_O = 2
DRAW = 3

class TicTacToeGame:
    def __init__(self):
        self.board = [[EMPTY, EMPTY, EMPTY] for _ in range(3)]
        self.ai_agent = Agent(PLAYER_O, learning=False)
        self.ai_agent.epsilon = 0
        self.load_trained_values()
    
    def is_valid_move(self, row, col):
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == EMPTY
    
    def make_move(self, row, col, player):
        if self.is_valid_move(row, col):
            self.board[row][col] = player
            return True
        return False
    
    def check_winner(self):
        for i in range(3):
            if self.board[i][0] != EMPTY and self.board[i][0] == self.board[i][1] == self.board[i][2]:
                return self.board[i][0]
            if self.board[0][i] != EMPTY and self.board[0][i] == self.board[1][i] == self.board[2][i]:
                return self.board[0][i]
        
        if self.board[0][0] != EMPTY and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] != EMPTY and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        
        if all(self.board[i][j] != EMPTY for i in range(3) for j in range(3)):
            return DRAW
        
        return None
    
    def ai_move(self):
        if self.check_winner():
            return None
        
        move = self.ai_agent.action(self.board)
        return move
    
    def get_move_values(self):
        move_values = {}
        if self.check_winner():
            return move_values
            
        maxval = -50000
        best_moves = []
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == EMPTY:
                    self.board[i][j] = PLAYER_O
                    val = self.ai_agent.lookup(self.board)
                    self.board[i][j] = EMPTY
                    move_values[f"{i},{j}"] = round(val, 4)
                    
                    if val > maxval:
                        maxval = val
                        best_moves = [(i, j)]
                    elif val == maxval:
                        best_moves.append((i, j))
        
        # Add info about tie-breaking
        if len(best_moves) > 1:
            move_values["_tie_info"] = f"Tied moves: {best_moves}, will choose randomly"
        
        return move_values
    
    def generate_game_tree(self, max_depth=None):
        """Generate complete game tree until game ends"""
        def create_tree_node(board, player, current_depth):
            winner = self.check_winner_for_board(board)
            if winner is not None:  # Game ended
                return None
            
            # Stop at max_depth if specified, but allow deeper generation for value calculation
            if max_depth is not None and current_depth > max_depth:
                return None
            
            node = {
                'board': deepcopy(board),
                'player': player,
                'moves': [],
                'depth': current_depth,
                'expanded': current_depth == 0  # Only root is expanded by default
            }
            
            # Generate all possible moves for current player
            for i in range(3):
                for j in range(3):
                    if board[i][j] == EMPTY:
                        # Create new board with this move
                        new_board = deepcopy(board)
                        new_board[i][j] = player
                        
                        # Get value based on player - use actual trained values
                        temp_board = deepcopy(board)
                        temp_board[i][j] = player
                        
                        # Get the state tuple key to check if it exists in trained values
                        state_key = self.ai_agent.statetuple(temp_board)
                        
                        if state_key in self.ai_agent.values:
                            # Use the actual trained value
                            value = self.ai_agent.values[state_key]
                        else:
                            # If not in trained values, evaluate the position more intelligently
                            winner = self.check_winner_for_board(temp_board)
                            if winner == self.ai_agent.player:
                                value = 1.0
                            elif winner == EMPTY:
                                # For non-terminal positions without trained values, use a basic heuristic
                                value = self.evaluate_position(temp_board, player)
                                # Ensure we don't return exactly 0 (which causes display issues)
                                if value == 0.0:
                                    value = 0.001
                            elif winner == DRAW:
                                value = 0.0
                            else:
                                value = self.ai_agent.lossval
                            
                        
                        # Create child node recursively (continue generating deeper levels)
                        child_node = create_tree_node(new_board, 3 - player, current_depth + 1)
                        
                        # Check if child node has moves
                        has_children = child_node is not None and child_node.get('moves') and len(child_node.get('moves', [])) > 0
                        
                        move_info = {
                            'position': (i, j),
                            'value': value,  # Use exact value, no rounding
                            'board': deepcopy(new_board),
                            'player': player,
                            'child': child_node,
                            'has_children': has_children
                        }
                        node['moves'].append(move_info)
                        
            
            # Sort moves by value
            if player == PLAYER_O:  # AI moves - highest first
                node['moves'].sort(key=lambda x: x['value'], reverse=True)
            else:  # Human moves - we can sort by human advantage
                node['moves'].sort(key=lambda x: x['value'], reverse=True)
            
            return node
        
        tree = create_tree_node(self.board, PLAYER_O, 0)
        return tree
    
    def evaluate_position(self, board, player):
        """Basic heuristic evaluation for positions without trained values"""
        # Simple evaluation based on potential wins and blocks
        score = 0.0
        
        # Check all lines (rows, columns, diagonals)
        lines = [
            # Rows
            [(0,0), (0,1), (0,2)], [(1,0), (1,1), (1,2)], [(2,0), (2,1), (2,2)],
            # Columns  
            [(0,0), (1,0), (2,0)], [(0,1), (1,1), (2,1)], [(0,2), (1,2), (2,2)],
            # Diagonals
            [(0,0), (1,1), (2,2)], [(0,2), (1,1), (2,0)]
        ]
        
        for line in lines:
            player_count = sum(1 for (i,j) in line if board[i][j] == player)
            opponent_count = sum(1 for (i,j) in line if board[i][j] == (3 - player))
            empty_count = sum(1 for (i,j) in line if board[i][j] == EMPTY)
            
            if player_count == 2 and empty_count == 1:
                score += 0.5  # Two in a row, can win
            elif player_count == 1 and empty_count == 2:
                score += 0.1  # One in a row, potential
            elif opponent_count == 2 and empty_count == 1:
                score -= 0.6  # Opponent can win, must block
            elif opponent_count == 1 and empty_count == 2:
                score -= 0.1  # Opponent has potential
        
        # Favor center position
        if board[1][1] == player:
            score += 0.2
        elif board[1][1] == (3 - player):
            score -= 0.2
            
        # Return a value between 0 and 1 (scaled and shifted)
        evaluated_value = max(0.001, min(0.999, 0.5 + score * 0.2))
        return evaluated_value
    
    def check_winner_for_board(self, board):
        """Check winner for a specific board state"""
        for i in range(3):
            if board[i][0] != EMPTY and board[i][0] == board[i][1] == board[i][2]:
                return board[i][0]
            if board[0][i] != EMPTY and board[0][i] == board[1][i] == board[2][i]:
                return board[0][i]
        
        if board[0][0] != EMPTY and board[0][0] == board[1][1] == board[2][2]:
            return board[0][0]
        if board[0][2] != EMPTY and board[0][2] == board[1][1] == board[2][0]:
            return board[0][2]
        
        if all(board[i][j] != EMPTY for i in range(3) for j in range(3)):
            return DRAW
        
        return None
    
    def get_state(self):
        return {
            'board': deepcopy(self.board),
            'ai_values': dict(self.ai_agent.values)
        }
    
    def load_state(self, state):
        self.board = deepcopy(state['board'])
        self.ai_agent.values = dict(state['ai_values'])
    
    def load_trained_values(self):
        try:
            import pickle
            with open('trained_agent_values.pkl', 'rb') as f:
                trained_values = pickle.load(f)
                self.ai_agent.values = trained_values
                print(f"Loaded {len(trained_values)} trained states")
        except FileNotFoundError:
            print("No trained values found. Using default untrained agent.")
        except Exception as e:
            print(f"Error loading trained values: {e}")
            print("Using default untrained agent.")

def enumstates(state, idx, agent):
    if idx > 8:
        player = last_to_act(state)
        if player == agent.player:
            agent.add(state)
    else:
        winner = gameover(state)
        if winner != EMPTY:
            return
        i = int(idx / 3)
        j = int(idx % 3)
        for val in range(3):
            state[i][j] = val
            enumstates(state, idx+1, agent)

def last_to_act(state):
    countx = 0
    counto = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == PLAYER_X:
                countx += 1
            elif state[i][j] == PLAYER_O:
                counto += 1
    if countx == counto:
        return PLAYER_O
    if countx == (counto + 1):
        return PLAYER_X
    return -1

def gameover(state):
    for i in range(3):
        if state[i][0] != EMPTY and state[i][0] == state[i][1] and state[i][0] == state[i][2]:
            return state[i][0]
        if state[0][i] != EMPTY and state[0][i] == state[1][i] and state[0][i] == state[2][i]:
            return state[0][i]
    if state[0][0] != EMPTY and state[0][0] == state[1][1] and state[0][0] == state[2][2]:
        return state[0][0]
    if state[0][2] != EMPTY and state[0][2] == state[1][1] and state[0][2] == state[2][0]:
        return state[0][2]
    for i in range(3):
        for j in range(3):
            if state[i][j] == EMPTY:
                return EMPTY
    return DRAW

class Agent:
    def __init__(self, player, verbose=False, lossval=0, learning=True):
        self.values = {}
        self.player = player
        self.verbose = verbose
        self.lossval = lossval
        self.learning = learning
        self.epsilon = 0.1
        self.alpha = 0.99
        self.prevstate = None
        self.prevscore = 0
        self.count = 0
        enumstates([[EMPTY,EMPTY,EMPTY],[EMPTY,EMPTY,EMPTY],[EMPTY,EMPTY,EMPTY]], 0, self)

    def episode_over(self, winner):
        self.backup(self.winnerval(winner))
        self.prevstate = None
        self.prevscore = 0

    def action(self, state):
        r = random.random()
        if r < self.epsilon:
            move = self.random(state)
        else:
            move = self.greedy(state)
        return move

    def random(self, state):
        available = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    available.append((i,j))
        return random.choice(available)

    def greedy(self, state):
        maxval = -50000
        best_moves = []
        
        for i in range(3):
            for j in range(3):
                if state[i][j] == EMPTY:
                    state[i][j] = self.player
                    val = self.lookup(state)
                    state[i][j] = EMPTY
                    
                    if val > maxval:
                        maxval = val
                        best_moves = [(i, j)]
                    elif val == maxval:
                        best_moves.append((i, j))
        
        # Random tie-breaking when multiple moves have same value
        maxmove = random.choice(best_moves) if best_moves else None
        
        self.backup(maxval)
        return maxmove
    
    def print_board(self, state):
        symbols = [' ', 'X', 'O']
        print("   0   1   2")
        for i in range(3):
            row = f"{i}  "
            for j in range(3):
                row += f"{symbols[state[i][j]]}   "
            print(row)

    def backup(self, nextval):
        if self.prevstate != None and self.learning:
            self.values[self.prevstate] += self.alpha * (nextval - self.prevscore)

    def lookup(self, state):
        key = self.statetuple(state)
        if not key in self.values:
            self.add(key)
        return self.values[key]

    def add(self, state):
        winner = gameover(state)
        tup = self.statetuple(state)
        self.values[tup] = self.winnerval(winner)

    def winnerval(self, winner):
        if winner == self.player:
            return 1
        elif winner == EMPTY:
            return 0.5
        elif winner == DRAW:
            return 0
        else:
            return self.lossval

    def statetuple(self, state):
        return (tuple(state[0]),tuple(state[1]),tuple(state[2]))