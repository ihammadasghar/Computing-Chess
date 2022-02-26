from models import Board


def minimax(position, destination, game_board, min_player, alpha=-500.0, beta=500.0, depth=4):
    board = Board(game_board.max_player, game_board.min_player)
    board.set_state(game_board)

    game_ended = board.make_move(position, destination)
    if depth == 0 or game_ended:
        return board.state

    if min_player:
        moves = board.max_player_moves
        max_state = -500.0
        pruned = False
        for position, destinations in moves.items():
            for destination in destinations:
                board_state = minimax(position, destination, board, False, alpha, beta, depth-1)
                max_state = max(max_state, board_state)
                alpha = max(alpha, board_state)
                if beta <= alpha:
                    pruned = True
                    break
            if pruned:
                break
        return max_state
        
    else:
        moves = board.min_player_moves
        min_state = 500.0
        pruned = False
        for position, destinations in moves.items():
            for destination in destinations:
                board_state = minimax(position, destination, board, True, alpha, beta, depth-1)
                min_state = min(min_state, board_state)
                beta = max(beta, board_state)
                if beta <= alpha:
                    pruned = True
                    break
            if pruned:
                break
        return min_state