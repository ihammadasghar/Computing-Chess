def print_board(board):
    print("................................................................................................................")
    board.evaluate_worths()
    for row in range(8):
        names = []
        for col in range(8):
            cell = board.cells[(row, col)]
            piece = cell.piece
            if piece:
                names.append(f"{piece.name[:1]}({row},{col}){cell.worth}")
            else:
                names.append("---------")
        print(names)

    for piece, position in board.piece_positions.items():
        print(piece.name, piece.team, position)
    white_moves = ""
    moves = board.max_player_moves
    for position, destination in moves:
        white_moves += f"\n{position}: "
        white_moves += f"{destination}, "

    black_moves = ""
    moves = board.min_player_moves
    for position, destination in moves:
        black_moves += f"\n{position}: "
        black_moves += f"{destination}, "

    print(f"\n\nBoard state: {board.state}\n\nPlayer white moves: {white_moves}\n\nPlayer black moves: {black_moves}")