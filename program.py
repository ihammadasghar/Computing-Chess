from models import Board, Player
from minimax import minimax
from utility import print_board

player_white = Player("Hammad", "white")
player_black = Player("Habib", "black")
board = Board(max_player=player_white, min_player=player_black)

    
while True:
    print_board(board)
    command = input("\nPosition Destination: ")
    command = command.split(" ")
    position = tuple(map(int, command[0].split(",")))
    destination = tuple(map(int, command[1].split(",")))
    new_board = board
    print(f"Minimax says: {minimax(position, destination, new_board)}")
    board.make_move(position, destination)
