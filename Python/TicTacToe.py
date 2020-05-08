import random

board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
player_1_name = ''
player_2_name = ''

def get_names():
    global player_1_name
    player_1_name = input("Player 1, enter your name: ")
    global player_2_name
    player_2_name = input("Player 2, now please enter your name: ")

def get_markers():
    player_1_symbol = ''
    global markers
    while player_1_symbol != 'X' and player_1_symbol != 'O':
        player_1_symbol = input(player_1_name + ", what would you prefer 'X' or 'O'?: ").upper()
        if player_1_symbol != 'X' and player_1_symbol != 'O':
            print("You must choose only between theese two!")
    print("OK, " + player_1_name + ", your symbol is " + player_1_symbol)
    symbols = ('X', 'O')
    for x in symbols:
        if player_1_symbol == symbols[0]:
            player_2_symbol = symbols[1]
        else:
            player_2_symbol = symbols[0]
    print("Got it, " + player_2_name + ", your symbol is " + player_2_symbol)
    if player_1_symbol == 'X':
        markers = ('X', 'O')
    else:
        markers = ('O', 'X')

def display_board(board):
    print('\n'*100)
    print('   |   |')
    print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
    print('   |   |')
    print('-----------')
    print('   |   |')
    print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
    print('   |   |')

def whos_first():
    if random.randint(0, 1) == 0:
        return player_1_name
    else:
        return player_2_name

def place_marker(player, place, board):
    while place not in range(1,10):
        place = int(input("Enter the correct number of cell (from 1 to 9): "))
    while board[place] != ' ':
        place = int(input("This cell is not empty! Choose another one: "))
    player_1_marker, player_2_marker = markers
    if player == player_1_name:
        board[place] = player_1_marker
        return board
    else:
        board[place] = player_2_marker
        return board

def check_spaces(board):
    if ' ' in board[1:]:
        return True
    else:
        return False

def winner_check(board, markers):
    player_1_marker, player_2_marker = markers
    if board[1] == board[2] == board[3] != ' ':
        if board[1] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    elif board[4] == board[5] == board[6] != ' ':
        if board[4] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    elif board[7] == board[8] == board[9] != ' ':
        if board[7] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    elif board[1] == board[4] == board[7] != ' ':
        if board[1] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    elif board[2] == board[5] == board[8] != ' ':
        if board[2] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    elif board[3] == board[6] == board[9] != ' ':
        if board[3] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    elif board[1] == board[5] == board[9] != ' ':
        if board[1] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    elif board[3] == board[5] == board[7] != ' ':
        if board[3] == player_1_marker:
            return player_1_name
        else:
            return player_2_name
    else:
        return False

def start_game(board):
    firstplayer = whos_first()
    print(firstplayer + " goes first!")
    display_board(board)
    place = int(input(firstplayer + ", where do you want to place you mark?\n(Choose the number of a cell, from 1 to 9): "))
    place_marker(firstplayer,place,board)
    free_cells = check_spaces(board)
    winner = winner_check(board,markers)
    while not winner and free_cells:
        display_board(board)
        p1marks = board.count(markers[0])
        p2marks = board.count(markers[1])
        if p1marks > p2marks:
            player = player_2_name
            place = int(input(player + ", now your turn. Where do you want to place you mark?\n(Choose the number of a cell, from 1 to 9): "))
            place_marker(player, place, board)
        elif p1marks < p2marks:
            player = player_1_name
            place = int(input(player + ", now your turn. Where do you want to place you mark?\n(Choose the number of a cell, from 1 to 9): "))
            place_marker(player, place, board)
        else:
            if firstplayer == player_1_name:
                player = player_1_name
            else:
                player = player_2_name
            place = int(input(player + ", now your turn. Where do you want to place you mark?\n(Choose the number of a cell, from 1 to 9): "))
            place_marker(player, place, board)
        free_cells = check_spaces(board)
        winner = winner_check(board, markers)
    if winner:
        display_board(board)
        print("Congrats, " + winner + ", you did it!")
    else:
        print("It's a draw!")
    rematch = input("Do you want a rematch? [Y/N]: ").upper()[0]
    if rematch == 'Y':
        board = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        start_game(board)
    else:
        print("Thanks for playing the game!")



get_names()
get_markers()
start_game(board)