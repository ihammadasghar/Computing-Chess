f = 10

class Pawn:
    def __init__(self, team) -> None:
        self.team = team
        self.points = 1 * f
        self.image = f"pawn-{team}.png"


    def calculate_range(self, position, board):
        cell = board.cells[position]
        team = cell.piece.team
        row, col = position
        destinations = [(row+1, col-1), (row+1, col+1)] if team == "white" else [(row-1, col-1), (row-1, col+1)]
        for destination in destinations:
            board.optimize_state(position, destination)
        
        forward = (row+1, col) if team == "white" else (row-1, col)
        fr, _ = forward
        if 0 <= fr <= 7:
            if board.cells[forward].piece is None:
                if team == "white":
                    board.max_player_moves.append((position, forward))
                else:
                    board.min_player_moves.append((position, forward))

        #  Initial pawn position double forward move
        double_forward = (row+2, col) if team == "white" else (row-2, col)
        dr, _ = double_forward
        if 0 <= dr <= 7:
            if board.cells[double_forward].piece is None and board.cells[forward].piece is None:
                if team == "white" and row == 1:
                    board.max_player_moves.append((position, double_forward))
                elif team == "black" and row == 6:
                    board.min_player_moves.append((position, double_forward))


class Knight:
    def __init__(self, team) -> None:
        self.team = team
        self.points = 3 * f
        self.image = f"knight-{team}.png"


    def calculate_range(self, position, board):
        row, col = position
        destinations = [(row-2, col-1), (row-2, col+1),
                    (row-1, col-2), (row-1, col+2),
                    (row+1, col-2), (row+1, col+2),
                    (row+2, col-1), (row+2, col+1),
                    ]
        for destination in destinations:
            board.optimize_state(position, destination)


class Bishop:
    def __init__(self, team) -> None:
        self.team = team
        self.points = 3 * f
        self.image = f"bishop-{team}.png"
    

    def calculate_range(self, position, board):
        row, col = position
        
        top_left, top_right, bottom_left, bottom_right = True, True, True, True
        for i in range(1, 8):
            if top_left:
                top_left = not board.optimize_state(position, (row-i, col-i))
            
            if top_right:
                top_right = not board.optimize_state(position, (row-i, col+i))

            if bottom_left:
                bottom_left = not board.optimize_state(position, (row+i, col-i))

            if bottom_right:
                bottom_right = not board.optimize_state(position, (row+i, col+i))

            if not(top_left or top_right or bottom_left or bottom_right):
                break


class Rook:
    def __init__(self, team) -> None:
        self.team = team
        self.points = 5 * f
        self.image = f"rook-{team}.png"
    

    def calculate_range(self, position, board):
        row, col = position

        up, down, left, right = True, True, True, True
        for i in range(1, 8):
            if up:
                up = not board.optimize_state(position, (row-i, col))
            
            if down:
                down = not board.optimize_state(position, (row+i, col))

            if left:
                left = not board.optimize_state(position, (row, col-i))

            if right:
                right = not board.optimize_state(position, (row, col+i))

            if not(left or right or up or down):
                break


class Queen:
    def __init__(self, team) -> None:
        self.team = team
        self.points = 10 * f
        self.image = f"queen-{team}.png"
    

    def calculate_range(self, position, board):
        row, col = position

        top_left, top_right, bottom_left, bottom_right = True, True, True, True
        up, down, left, right = True, True, True, True
        for i in range(1, 8):
            if up:
                up = not board.optimize_state(position, (row-i, col))
            
            if down:
                down = not board.optimize_state(position, (row+i, col))

            if left:
                left = not board.optimize_state(position, (row, col-i))

            if right:
                right = not board.optimize_state(position, (row, col+i))

            if top_left:
                top_left = not board.optimize_state(position, (row-i, col-i))
            
            if top_right:
                top_right = not board.optimize_state(position, (row-i, col+i))

            if bottom_left:
                bottom_left = not board.optimize_state(position, (row+i, col-i))

            if bottom_right:
                bottom_right = not board.optimize_state(position, (row+i, col+i))

            if not(left or right or up or down or top_left or top_right or bottom_left or bottom_right):
                break


class King:
    def __init__(self, team) -> None:
        self.team = team
        self.points = 500
        self.image = f"king-{team}.png"
    
    def calculate_range(self, position, board):
        row, col = position
        destinations = [(row+1, col-1), (row+1, col), (row+1, col+1), 
                    (row, col-1), (row, col+1), 
                    (row-1, col-1), (row-1, col), (row-1, col+1),]
        for destination in destinations:
            board.optimize_state(position, destination)