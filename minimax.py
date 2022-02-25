from models import Board, Player
from utility import print_board

def minimax(position, destination, game_board, depth_calculated=0, depth=5):
    board = Board(Player("h", "white"), Player("h", "black"))
    board.set_state(game_board)

    row, col = position
    cell = board.cells[row][col]
    min_player = False if cell.piece.team == "white" else True
    game_ended = board.make_move(position, destination)

    

    if depth_calculated == depth or game_ended:
        return board.state

    if  min_player:
        moves = board.max_player.possible_moves
        max_out = -1000
        for position in moves.keys():
            for destination in moves[position]:
                outcome = minimax(position, destination, board, depth_calculated=depth_calculated+1)
                max_out = max(max_out, outcome)
        return max_out
    else:
        moves = board.min_player.possible_moves
        min_out = 1000
        for position in moves.keys():
            for destination in moves[position]:
                outcome = minimax(position, destination, board, depth_calculated=depth_calculated+1)
                min_out = min(min_out, outcome)
        return min_out