import sys
import core

# Players
player_str = {core.WHITE: 'white', core.BLACK: 'black'}

board = core.get_new_board()
player = core.WHITE
moves = []

print('Hi! I hope you are ready to play!')
print('To make a move, write the start coordinates of the piece you want to move, and then the end coordinates. The syntax for a coordinate is "ROW,COLUMN".')
print('Good luck to you both!')
print()
print(board)
print()

while(True): 
    if core.is_checked(board, player):
        if core.is_check_mated(board, player, moves):
            print('Check mate!')
            print('%s wins!' % player_str[-player])
            break
        print('You are in check!') 
    print('It\'s your turn %s, what\'s your move?' % player_str[player])
    try:
        start = list(map(lambda x: int(x), str(input()).split(',')))
        end = list(map(lambda x: int(x), str(input()).split(',')))
    except KeyboardInterrupt:
        print()
        print('Sad to see you go :(')
        sys.exit()
    except:
        print('I could not understand that... The format for a coordinate is "ROW,COLUMN".')
        continue
    if len(start) != 2 or len(end) != 2:
        print('This is 2D chess...')
        continue
    if core.is_legal(board, player, moves, [start, end]):
        core.make_move(board, player, moves, [start, end])
        print()
        print(board)
        print()
        moves.append([start, end])
        player = -player
        continue
    else:
        print('That\'s illegal!')
        continue
