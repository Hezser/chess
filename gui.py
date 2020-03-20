import pygame
import copy
import core

# Sizes
SIZE = WIDTH, HEIGHT = 640, 640
SQUARE_SIZE = 80

# Images
imgs = { core.WHITE_PAWN: 'assets/white_pawn.png',
         core.BLACK_PAWN: 'assets/black_pawn.png',
         core.WHITE_KNIGHT: 'assets/white_knight.png',
         core.BLACK_KNIGHT: 'assets/black_knight.png',
         core.WHITE_BISHOP: 'assets/white_bishop.png',
         core.BLACK_BISHOP: 'assets/black_bishop.png',
         core.WHITE_ROOK: 'assets/white_rook.png',
         core.BLACK_ROOK: 'assets/black_rook.png',
         core.WHITE_QUEEN: 'assets/white_queen.png',
         core.BLACK_QUEEN: 'assets/black_queen.png',
         core.WHITE_KING: 'assets/white_king.png',
         core.BLACK_KING: 'assets/black_king.png' }

class ContinueGame(Exception):
   pass

class BreakGame(Exception):
    pass

def draw_board(window):
    colors = [(232, 235, 239), (125, 135, 150)]
    c = 0
    for x in range(8):
        for y in range(8):
            pygame.draw.rect(window, colors[c], (x*SQUARE_SIZE, y*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if y != 7:
                c = (c+1) % 2

def update_board(board, window):
    window.fill((0, 0, 0))
    draw_board(window)
    for x in range(8):
        for y in range(8):
            piece = board[x][y]
            if piece != core.FREE:
                img = pygame.image.load(imgs[piece]).convert_alpha()
                window.blit(img, (y*SQUARE_SIZE, x*SQUARE_SIZE))
    pygame.display.update()

def translate_position(pos):
    res = []
    res.append(int(pos[1]/SQUARE_SIZE))
    res.append(int(pos[0]/SQUARE_SIZE))
    return res

def play_game():
    pygame.init()
    window = pygame.display.set_mode(SIZE)
    board = core.get_new_board()
    player = core.WHITE
    boards = [copy.deepcopy(board)]
    moves = []
    draw_board(window)
    update_board(board, window)
    move_state = core.START
    move = []
    while(True):
        try:
            ev = pygame.event.get()
            for event in ev:
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = translate_position(pygame.mouse.get_pos())
                    if move_state == core.START:
                        move = []
                        move.append(pos)
                        move_state = core.END
                    else:
                        move.append(pos)
                        move_state = core.START
                        if core.make_move(board, player, moves, move): 
                            update_board(board, window)
                            boards.append(copy.deepcopy(board))
                            moves.append(move)
                            player = -player
                            if core.is_checked(board, player):
                                print('Check!')
                                if core.is_check_mated(board, player, moves):
                                    print('Check mate!')
                                    raise BreakGame
                            if core.is_a_draw(board, player, boards, moves):
                                print('It\'s a draw!')
                                raise BreakGame
                        else:
                            raise ContinueGame
        except ContinueGame:
            continue
        except BreakGame:
            break
play_game()
