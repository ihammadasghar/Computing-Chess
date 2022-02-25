from models import Board, Player
from utility import print_board

def minimax(position, destination, game_board, alpha=-1000, beta=1000, depth=4):
    board = Board(Player("h", "white"), Player("h", "black"))
    board.set_state(game_board)

    row, col = position
    cell = board.cells[row][col]
    min_player = False if cell.piece.team == "white" else True
    game_ended = board.make_move(position, destination)

    if depth == 0 or game_ended:
        return board.state

    if  min_player:
        moves = board.max_player.possible_moves
        max_state = -1000
        prunned = False
        for position in moves.keys():
            for destination in moves[position]:
                board_state = minimax(position, destination, board, alpha, beta, depth-1)
                max_state = max(max_state, board_state)
                alpha = max(alpha, board_state)
                if beta <= alpha:
                    break
            if prunned:
                break

        return max_state
    else:
        moves = board.min_player.possible_moves
        min_state = 1000
        prunned = False
        for position in moves.keys():
            for destination in moves[position]:
                board_state = minimax(position, destination, board, alpha, beta, depth-1)
                min_state = min(min_state, board_state)
                beta = max(beta, board_state)
                if beta <= alpha:
                    break
            if prunned:
                break
        return min_state