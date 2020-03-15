import numpy as np
import copy

# TODO: Stalemate detection
# TODO: Implement pawn promotions
# TODO: Implement weird pawn rule

# Board
ROW = 0
COL = 1

# Players
WHITE = 1
BLACK = -1

# Move
START = 0
END = 1

# Direction
STRAIGHT = 0
DIAGONAL = 1

# Pieces
FREE = 0
WHITE_PAWN = PAWN = 1
WHITE_KNIGHT = KNIGHT = 2
WHITE_BISHOP = BISHOP = 3
WHITE_ROOK = ROOK = 4
WHITE_QUEEN = QUEEN = 5
WHITE_KING = KING = 6
BLACK_PAWN = -1
BLACK_KNIGHT = -2
BLACK_BISHOP = -3
BLACK_ROOK = -4
BLACK_QUEEN = -5
BLACK_KING = -6

class game:
    def __init__(self, board, moves):
        self.board = board
        self.moves = moves

    def __init__(self):
        self.board = get_new_board()
        self.moves = []
    
    def get_board():
        return self.board

    def get_moves():
        return self.moves

    def add_move(move):
        moves.append(move)

# Black is rows 0,1 and white is rows 6,7 initially
def get_new_board():
    board = np.zeros((8,8), dtype=int)
    board[1] = board[6] = np.ones((8), dtype=int)
    board[0] = board[7] = [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]
    board[0] = board[0] * -1
    board[1] = board[1] * -1
    return board

def make_move(board, player, prev_moves, move):
    if not is_legal(board, player, prev_moves, move):
        return False
    # Castle
    if abs(board[move[START][ROW]][move[START][COL]]) == KING and abs(move[START][COL]-move[END][COL]) == 2:
        board[move[END][ROW]][move[END][COL]] = board[move[START][ROW]][move[START][COL]]
        rook_start_pos = [((-player) % 9) - 1, (int((move[START][COL]-move[END][COL])/2) % 9) - 1]
        rook_end_pos = [((-player) % 9) - 1, (int((move[START][COL]-move[END][COL])/2) % 4) + 2]
        board[rook_end_pos[ROW]][rook_end_pos[COL]] = board[rook_start_pos[ROW]][rook_start_pos[COL]]
        board[move[START][ROW]][move[START][COL]] = FREE
        board[rook_start_pos[ROW]][rook_start_pos[COL]] = FREE
    else:
        board[move[END][ROW]][move[END][COL]] = board[move[START][ROW]][move[START][COL]]
        board[move[START][ROW]][move[START][COL]] = FREE
    return True

def is_legal(board, player, prev_moves, move):
    start = move[START]
    end = move[END]
    # Move is not within the board
    if end[ROW] < 0 or end[ROW] > 7 or end[COL] < 0 or end[COL] > 7:
        print('A move outside the board...')
        return False   
    piece = board[start[ROW]][start[COL]]
    end_square_piece = board[end[ROW]][end[COL]]
    # Static move, stupid move
    if start == end:
        print('A static move...')
        return False 
    # Cannot move an empty square
    if piece == FREE:
        print('Trying to move a free square...')
        return False
    # Cannot move your opponent's pieces
    if player * piece < 0:
        print('Trying to move your opponent\'s piece...')
        return False
    # Cannot move on top of friendly piece
    else:
        if end_square_piece * piece > 0:
            print('Trying to eat your own piece...')
            return False
    res = False
    if piece == WHITE_PAWN or piece == BLACK_PAWN:
        move_once = start[ROW] == (end[ROW] + piece) and start[COL] == end[COL] and end_square_piece == FREE
        move_twice = (-piece) % 7 == start[ROW] and start[ROW] == (end[ROW] + 2*piece) and start[COL] == end[COL] and board[end[ROW]-1][end[COL]] == FREE and end_square_piece == FREE
        eat = start[ROW] == (end[ROW] + piece) and abs(start[COL] - end[COL]) == 1 and end_square_piece != FREE
        res = move_once or move_twice or eat
    piece = abs(piece)
    if piece == KNIGHT:
        ver = abs(start[ROW] - end[ROW])
        hor = abs(start[COL] - end[COL])
        res = (ver == 2 and hor == 1) or (ver == 1 and hor == 2)
    elif piece == BISHOP:
        res = abs(start[ROW] - end[ROW]) == abs(start[COL] - end[COL]) and is_path_clear(board, [start, end], DIAGONAL)
        print(res)
    elif piece == ROOK:
        res = (start[ROW] == end[ROW] or start[COL] == end[COL]) and is_path_clear(board, [start, end], STRAIGHT)
    elif piece == QUEEN:
        res = ((start[ROW] == end[ROW] or start[COL] == end[COL]) and is_path_clear(board, [start, end], STRAIGHT)) or \
                (abs(start[ROW] - end[ROW]) == abs(start[COL] - end[COL]) and is_path_clear(board, [start, end], DIAGONAL))
    elif piece == KING:
        ver = abs(start[ROW] - end[ROW])
        hor = abs(start[COL] - end[COL])
        castle = False
        if abs(start[COL]-end[COL]) == 2:
            moved_pieces = False
            king_pos = [((-player) % 9) - 1, 4]
            rook_pos = [((-player) % 9) - 1, (int((start[COL]-end[COL])/2) % 9) - 1]
            for prev_move in prev_moves:
                if prev_move[START] == king_pos or prev_move[START] == rook_pos:
                    moved_pieces = True
            castle = start[ROW] == end[ROW] and is_path_clear(board, [king_pos, rook_pos], STRAIGHT) and not moved_pieces
        res = (ver == 1 and hor == 1) or ver + hor == 1 or castle
    # If that move gets the player in check
    if res:
        next_board = copy.deepcopy(board)
        next_board[end[ROW]][end[COL]] = next_board[start[ROW]][start[COL]]
        next_board[start[ROW]][start[COL]] = FREE
        res = not is_checked(next_board, player)
        if not res:
            print('That move gets you in check...')
    return res

# path is two different coordinates, direction is either STRAIGHT or DIAGONAL. Returns true if there is no piece along the path between the two coordinates
def is_path_clear(board, path, direction):
    start = path[START]
    end = path[END]
    if start == end:
        return True
    if direction == STRAIGHT:
        if start[COL] == end[COL]:  # Vertical
            ori = ROW
        else:  # Horizontal
            ori = COL
        if start[ori] > end[ori]:
            tmp = start
            start = end
            end = tmp
        for i in range(start[ori]+1, end[ori]):
            if ori == ROW:
                piece = board[i][start[COL]]
            else:
                piece = board[start[ROW]][i]
            if piece != FREE:
                return False
    else:
        if start[ROW] - end[ROW] == start[COL] - end[COL]:  # Top-down
            x = 1
        else:  # Bottom-up
            x = -1
        if start[ROW] > end[ROW]:
            tmp = start
            start = end
            end = tmp
        for i in range(1, end[ROW] - start[ROW]):
            if board[ROW+i][COL+(i*x)] != FREE:
                return False
    return True

def is_check_mated(board, player, prev_moves):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece * player < 0:
                tests = get_possible_moves(board, player, prev_moves, [row, col])
                for move in tests:
                    test_board = make_move(copy.deepcopy(board), player, prev_moves, move)
                    if not is_checked(test_board, player):
                        return False
    return True

def get_possible_moves(board, player, prev_moves, start):
    piece = abs(board[start[ROW]][start[END]])
    ends = []
    moves = []
    if piece == PAWN:
        ends = [ [start[ROW]+1, start[COL]], [start[ROW]+2, start[COL]], [start[ROW]-1, start[COL]], [start[ROW]-2, start[COL]], \
                [start[ROW]+1, start[COL]+1], [start[ROW]+1, start[COL]-1], [start[ROW]-1, start[COL]+1], [start[ROW]-1, start[COL]-1] ]
    elif piece == KNIGHT:
        ends = [ [start[ROW]+1, start[COL]+2], [start[ROW]+1, start[COL]-2], [start[ROW]-1, start[COL]+2], [start[ROW]-1, start[COL]-2], \
                [start[ROW]+2, start[COL]+1], [start[ROW]+2, start[COL]-1], [start[ROW]-2, start[COL]+1], [start[ROW]-2, start[COL]-1] ]
    elif piece == BISHOP or piece == QUEEN:
        for x in range(-7, 8):
            for y in range(-7, 8):
                ends.append([start[ROW]+x, start[COL]+y])
    if piece == ROOK or piece == QUEEN:
        for x in range(-7, 8):
            ends.append([start[ROW]+x, start[COL]])
            ends.append([start[ROW], start[COL]+x])
    elif piece == KING:
        ends = [ [start[ROW]-1, start[COL]], [start[ROW]-1, start[COL]+1], [start[ROW], start[COL]+1], [start[ROW]+1, start[COL]+1], \
                [start[ROW]+1, start[COL]], [start[ROW]+1, start[COL]-1], [start[ROW], start[COL]-1], [start[ROW]-1, start[COL]-1] ]
    for end in ends:
        if is_legal(board, player, prev_moves, [start, end]):
            moves.append([start, end])
    return moves

def is_checked(board, player):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece * player < 0:
                piece = abs(piece)
                if piece == PAWN:
                    if row+player >= 0 and row+player <= 7 and \
                            ((col+1 >= 0 and col+1 <= 7 and board[row+player][col+1] == player*KING) or \
                            (col-1 >= 0 and col-1 <= 7 and board[row+player][col-1] == player*KING)):
                        return True
                elif piece == KNIGHT:
                    for ver in [row-2, row-1, row+1, row+2]:
                        for hor in [col-2, col-1, col+1, col+2]:
                            if not (hor < 0 or hor > 7 or ver < 0 or ver > 7):  # Not outside the board
                                if board[ver][hor] == player*KING:
                                    return True
                elif piece == BISHOP or piece == ROOK or piece == QUEEN:
                    if piece == BISHOP:
                        coords = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
                    elif piece == ROOK:
                        coords = [[-1, 0], [1, 0], [0, -1], [0, 1]]
                    elif piece == QUEEN:
                        coords = [[-1, -1], [-1, 1], [1, -1], [1, 1], [-1, 0], [1, 0], [0, -1], [0, 1]]
                    while len(coords) > 0:
                        coord = coords[0]
                        test_row = row + coord[ROW]
                        test_col = col + coord[COL]
                        if test_row < 0 or test_row > 7 or test_col < 0 or test_col > 7:  # Not within the board
                            coords.remove(coord)
                            continue
                        elif board[coord[ROW]][coord[COL]] == player*KING:
                            return True
                        elif board[coord[ROW]][coord[COL]] == FREE:  # Keep traversing in the same direction
                            coords.remove(coord)
                            coords.append([coord[ROW] + np.sign(coord[ROW]), coord[ROW] + np.sign(coord[ROW])])
                        else:  # Stop traversing this direction
                            coords.remove(coord)
                elif piece == KING:  # Useful when checking that a player cannot move its king next to the other player's king
                    coords = [[-1, -1], [-1, 1], [1, -1], [1, 1], [-1, 0], [1, 0], [0, -1], [0, 1]]
                    for coord in coords:
                        test_row = row+coord[ROW]
                        test_col = col+coord[COL]
                        if test_row >= 0 and test_row <= 7 and test_col >= 0 and test_col <= 7 and board[test_row][test_col] == player*KING:
                            return True
    return False

