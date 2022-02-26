def print_board(board):
    print("................................................................................................................")
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

    white_moves = ""
    moves = board.max_player_moves
    for position in moves.keys():
        white_moves += f"\n{position}: "
        for destination in moves[position]:
            white_moves += f"{destination}, "

    black_moves = ""
    moves = board.min_player_moves
    for position in moves.keys():
        black_moves += f"\n{position}: "
        for destination in moves[position]:
            black_moves += f"{destination}, "

    print(f"\n\nBoard state: {board.state}\n\nPlayer white moves: {white_moves}\n\nPlayer black moves: {black_moves}")