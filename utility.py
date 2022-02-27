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

    print(f"\n\nBoard state: {board.state}\n")