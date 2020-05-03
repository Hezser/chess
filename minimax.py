import core
import copy

# Infinities
POSINF =  1000
NEGINF = -1000

# Evaluation function
EVAL = [0, 1, 3, 3, 5, 9, 100]

# Depth of search tree
MAX_DEPTH = 3

def get_move(board, player, prev_moves):
    possible_moves = core.get_possible_moves(board, player, prev_moves)
    vals = [minimax(core.make_move(copy.deepcopy(board), player, prev_moves, move), player, -player, copy.deepcopy(prev_moves) + [move], MAX_DEPTH, NEGINF, POSINF) for move in possible_moves]
    max_val = max(vals)
    return possible_moves[vals.index(max_val)]

def minimax(board, max_player, turn, prev_moves, depth, alpha, beta):
    if depth == 0:
        return evaluate(board)
    possible_moves = core.get_possible_moves(board, turn, prev_moves)
    if len(possible_moves) == 0:
        return (max_player*turn) * (-100)
    if max_player == turn:
        val = NEGINF
        for move in possible_moves: 
            val = max(val, minimax(core.make_move(copy.deepcopy(board), turn, prev_moves, move), max_player, -turn, copy.deepcopy(prev_moves) + [move], depth-1, alpha, beta))
            alpha = max(alpha, val)
            if alpha >= beta:
                break
        return val
    else:
        val = POSINF
        for move in possible_moves: 
            val = min(val, minimax(core.make_move(copy.deepcopy(board), turn, prev_moves, move), max_player, -turn, copy.deepcopy(prev_moves) + [move], depth-1, alpha, beta))
            beta = min(beta, val)
            if alpha >= beta:
                break
        return val

def evaluate(board):
    val = 0
    for row in range(8):
        for col in range(8):
            val += EVAL[board[row][col]]
    return val
