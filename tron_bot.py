import time
import sys

from typing import Literal, Tuple, Dict
from queue import Queue
import numpy as np

def flood_fill(state: np.ndarray, position: Tuple[int, int], scale_factor: float = 0.1, lazy: bool = False, iteration: int = 0) -> int:
    """
     BFS Based Flood Fill Algorithm Implemented with Queue, with the ability to change mode to Lazy Flood Fill.
    
    Args:
        state: The board configuration.
        position: The origin of flood fill algorithm        
        scale_factor: The scaling factor, between 0 and 1.
        lazy: Enabling Lazy Flood Fill Algorithm.
    Returns:
        An integer presenting the number of cells filled.
    """
    assert 0 <= scale_factor <= 1
    
    cells_left = 600 - 2*iteration
    max_count = max(10, int(cells_left * scale_factor))
    
    queue = Queue() 
    
    queue.put(position)
    visited = [position]
    space_count = 1 # the start position itself occupies one cell.
    
    # Expansion Order: D, U, R, L
    while not queue.empty():
        if lazy and (space_count >= max_count):
            break
        coord = queue.get()
        possible_moves:Dict[Literal['RIGHT', 'UP', 'LEFT', 'DOWN'], Tuple[int, int]] = get_actions(state, coord)
        
        for pos in possible_moves.values():
            if pos not in visited:
                visited.append(pos)
                queue.put(pos)
                space_count += 1
                if lazy and (space_count >= max_count):
                    break
                
    return space_count
        
    
    

def evaluate_state(state: np.ndarray, my_pos: Tuple[int, int], opp_pos: Tuple[int, int], scale_factor: float = 0.1, lazy: bool=False, iteration: int = 0) -> int:
    """
    Evaluation Function of the Minimax Algorithm
    
    Args:
        state: The board configuration.
        my_pos: The position of my agent.
        opp_pos: The position of opponent agent.
        scale_factor: The scaling factor, between 0 and 1.
        lazy: Enabling Lazy Flood Fill Algorithm.
        
    Returns:
        An integer presenting how interesting the state is for us.
    """
    my_space = flood_fill(state, position=my_pos, scale_factor=scale_factor, lazy=lazy, iteration=iteration)
    opp_space = flood_fill(state, position=opp_pos, scale_factor=scale_factor, lazy=lazy, iteration=iteration)
    
    return my_space - opp_space

def min_max(state: np.ndarray, my_pos: Tuple[int, int], opp_pos: Tuple[int, int], depth, max_mode: bool, alpha, beta, scale_factor: float = 0.1, lazy: bool=False, iteration: int = 0)  -> Tuple[int, Literal['RIGHT', 'UP', 'LEFT', 'DOWN']]:
    """
    This function performs minimax algorithm with alpha-beta-pruning.
    
    Args:
        state: The board configuration.
        my_pos: The position of my agent.
        opp_pos: The position of opponent agent.
        depth: The depth limit of minimax.
        max_mode: If True, we are at the max node, otherwise, in the min node.
        alpha: alpha value (for max node) of alpha-beta pruning.
        beta: beta value (for min node) of alpha-beta pruning.
        scale_factor: The scaling factor, between 0 and 1.
        lazy: Enabling Lazy Flood Fill Algorithm.
        
    Returns:
        The best action and its score for the given state.
    """
    # Base case
    if depth == 0:
        val = evaluate_state(state, my_pos=my_pos, opp_pos=opp_pos, scale_factor=scale_factor, lazy=lazy, iteration=iteration)
        return val, None
    
    if max_mode:
        possible_moves = get_actions(state, my_pos)
        best_action = ''
        best_score = float('-inf')
        player_number = 0
    else:
        possible_moves = get_actions(state, opp_pos)
        best_action = ''
        best_score = float('inf')
        player_number = 1
        
    # This means game over
    if len(possible_moves) == 0:
        val = evaluate_state(state, my_pos=my_pos, opp_pos=opp_pos, scale_factor=scale_factor, lazy=lazy, iteration=iteration)
        return val, None
    
    for action, next_coord in possible_moves.items():
        # The state given to minimax calls
        forward_state = state.copy()
        
        forward_state[next_coord[1], next_coord[0]] = player_number
        
        if max_mode:
            val, _ = min_max(state=forward_state, my_pos=next_coord, opp_pos=opp_pos, depth=depth - 1,  max_mode=False, alpha=alpha, beta=beta, scale_factor=scale_factor, lazy=lazy, iteration=iteration + 1)
        else:
            val, _ = min_max(state=forward_state, my_pos=my_pos, opp_pos=next_coord, depth=depth - 1,  max_mode=True, alpha=alpha, beta=beta, scale_factor=scale_factor, lazy=lazy, iteration=iteration + 1)
        
        if max_mode:
            if val > best_score:
                best_score = val
                best_action = action
                
            # Updating alpha
            alpha = max(best_score, alpha)
        else:
            if val < best_score:
                best_score = val
                best_action = action    
                
            # Updating beta
            beta = min(best_score, beta)
            
            
        if alpha >= beta:
            break
    return best_score, best_action        
        

def update_state(state: np.ndarray, player_number) -> np.ndarray:
    """
    This function updated the state variable, when an opponent has lost.
    
    Args:
        state: The board configuration.
        player_number: The number of the player in the board config.
        
    Returns:
        An updated state variable.
    """
    state[state == player_number] = -1
    
    return state

def get_actions(state: np.ndarray, position: Tuple[int, int]) ->  Dict[Literal['RIGHT', 'UP', 'LEFT', 'DOWN'], Tuple[int, int]]:
    """
    Returns the possible actions and their corresponding coords for the given position.
    """
    x, y = position
    max_x = state.shape[1]
    max_y = state.shape[0]
   
# Define moves and directly check validity
    moves = {
        'RIGHT': (x + 1, y) if x + 1 < max_x and state[y, x + 1] == -1 else None,
        'DOWN': (x, y + 1) if y + 1 < max_y and state[y + 1, x] == -1 else None,
        'LEFT': (x - 1, y) if x - 1 >= 0 and state[y, x - 1] == -1 else None,
        'UP': (x, y - 1) if y - 1 >= 0 and state[y - 1, x] == -1 else None
    }
    
    # Filter out invalid moves in a single step
    return {action: coord for action, coord in moves.items() if coord is not None}

if __name__ == '__main__':
    h, w = (20, 30)
    state = np.zeros((h, w)) - 1 # w, h

    # game loop
    while True:
        # n: total number of players (2 to 4).
        # p: your player number (0 to 3).
        try:
            n, p = [int(i) for i in input().split()]
        except EOFError:
            sys.exit(0)
        
        positions = [0 for i in range(n)] # each index contains the current coordinate of agent number i
        for i in range(n):
            # Input coordinations
            try:
                x0, y0, x1, y1 = list(map(int, input().split()))
            except EOFError:
                sys.exit(0)
            
            if x0 == -1:
                state = update_state(state, i)
            else:
                state[y1, x1] = i
                positions[i] = (x1, y1)
        if p == 0:
            t0 = time.time()
            best_value, best_action = min_max(
                state=state,
                my_pos=positions[0],
                opp_pos=positions[1],
                depth=5,
                max_mode=True,
                alpha=float('-inf'),
                beta=float('inf'),
                scale_factor=0.1,
                lazy=True,
                iteration=0
            )
            t1 = time.time()
            elapsed_ms = (t1 - t0) * 1000  # convert to ms

            print('=================')
            print('<<<<<<< Best Action >>>>>>>')
            print(best_action)
            print('<<<<<<< Elapsed Time >>>>>>>')
            elapsed = t1 - t0
            if elapsed < 1:
                print(f"{elapsed * 1000:.2f} ms")
            else:
                print(f"{elapsed:.2f} s")