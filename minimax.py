import core
import copy

# Evaluation function
EVAL = [0, 1, 3, 3, 5, 9, 100]

# Depth of search tree
MAX_DEPTH = 3

def get_move(board, player, prev_moves):
    possible_moves = core.get_possible_moves(board, player, prev_moves)
    vals = [minimax(core.make_move(copy.deepcopy(board), player, prev_moves, move), player, -player, copy.deepcopy(prev_moves) + [move], 1) for move in possible_moves]
    max_val = max(vals)
    return possible_moves[vals.index(max_val)]

def minimax(board, player, turn, prev_moves, depth):
    if depth == MAX_DEPTH:
        return evaluate(board, player)
    possible_moves = core.get_possible_moves(board, turn, prev_moves)
    if len(possible_moves) == 0:
        return -100
    return max(list(map(lambda move: minimax(core.make_move(copy.deepcopy(board), turn, prev_moves, move), player, -turn, copy.deepcopy(prev_moves) + [move], depth+1), possible_moves)))

def evaluate(board, player):
    val = 0
    for row in range(8):
        for col in range(8):
            val += player * EVAL[board[row][col]]
    return val

# For each possible immediate move, run minimax on it
# Minimax will, at each level of depth, (if at max_depth) return the valuation of the board or (if not at max_depth) run recursively minimax on all possible moves from the board and for a player in turn and return the max valuation they return


# WE ARE NOT ASSUMING THAT THE OTHER PLAYER WILL MAKE THE BEST MOVE POSSIBLE
