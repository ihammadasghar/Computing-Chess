from models import Board

def minimax(position, destination, game_board, max_player, alpha=float("-inf"), beta=float("inf"), depth=4):
    board = Board()
    board.set_state(game_board)
    board.make_move(position, destination)
    
    if depth == 0 or board.game_over:
        return board.state

    if max_player:
        min_state = float("inf")
        for position, destination in board.min_player_moves:
            board_state = minimax(position, destination, board, False, alpha, beta, depth-1)
            min_state = min(min_state, board_state)
            beta = min(beta, min_state)
            if beta <= alpha:
                break
        return min_state
        
    else:
        max_state = float("-inf")
        for position, destination in board.max_player_moves:
            board_state = minimax(position, destination, board, True, alpha, beta, depth-1)
            max_state = max(max_state, board_state)
            alpha = max(alpha, max_state)
            if beta <= alpha:
                break
        return max_state