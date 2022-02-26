from models import Board, Player, Piece
from minimax import minimax
from utility import print_board
from datetime import datetime

player_white = Player("Hammad", "white")
player_black = Player("Habib", "black")
board = Board(player_white, player_black)

pieces = [("rook", 5.0),
        ("knight", 3.0), 
        ("bishop", 3.0),
        ("king", 80.0),
        ("queen", 10.0),
        ("bishop", 3.0), 
        ("knight", 3.0), 
        ("rook", 5.0)]
pawn = ("pawn", 1.0)
teams = ("white", "black")

for i in range(8):
    name, worth = pieces[i]
    board.cells[(0, i)].piece = Piece(name, teams[0], worth)
    board.cells[(1, i)].piece = Piece(pawn[0], teams[0], pawn[1])
    board.cells[(7, i)].piece = Piece(name, teams[1], worth)
    board.cells[(6, i)].piece = Piece(pawn[0], teams[1], pawn[1])

while True:
    print_board(board)
    command = input("\nPosition Destination: ")
    command = command.split(" ")
    position = tuple(map(int, command[0].split(",")))
    destination = tuple(map(int, command[1].split(",")))
    new_board = board
    time_before = datetime.now()
    print(f"Minimax says: {minimax(position, destination, new_board, min_player=True)}")
    print("Time taken: ",datetime.now() - time_before)
