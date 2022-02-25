class Player:
    def __init__(self, name, team) -> None:
        self.name = name
        self.team = team
        self.possible_moves = {}


class Cell:
    def __init__(self, position, piece=None) -> None:
        self.piece = piece
        self.position = position


class Piece:
    def __init__(self, name, team, points) -> None:
        self.name = name
        self.team = team
        self.points = points
        self.worth = points
        self.possible_moves = []


class Board:
    def __init__(self, max_player=None, min_player=None) -> None:
        self.cells = [[Cell(position=(row,col)) for col in range(8)] for row in range(8)]
        self.max_player = max_player
        self.min_player = min_player
        self.state = 0.0
        self.history = []
        pieces = [
        ("rook", 5.0),
        ("knight", 3.0), 
        ("bishop", 3.0),
        ("king", 80.0),
        ("queen", 10.0),
        ("bishop", 3.0), 
        ("knight", 3.0), 
        ("rook", 5.0)
        ]

        for i in range(8):
            name, worth = pieces[i]
            self.cells[0][i].piece = Piece(name, "white", worth)
            self.cells[1][i].piece = Piece("pawn", "white", 1.0)
            self.cells[7][i].piece = Piece(name, "black", worth)
            self.cells[6][i].piece = Piece("pawn", "black", 1.0)

        self.evaluate_worths()


    def set_state(self, board):
        self.max_player = board.max_player
        self.min_player = board.min_player
        self.state = board.state
        for position, destination in board.history:
            self.make_move(position, destination)


    def make_move(self, position, destination):
        self.history.append((position, destination))

        prow, pcol = position
        drow, dcol = destination
        piece = self.cells[prow][pcol].piece
        if piece == "white":
            self.state -= (piece.worth - piece.points)
        else:
            self.state += (piece.worth - piece.points)
        self.cells[prow][pcol].piece = None

        destination_piece = self.cells[drow][dcol].piece
        #  Capturing
        if destination_piece:
            if destination_piece.team == "white":
                self.state -= (destination_piece.worth - destination_piece.points)
                self.state -= destination_piece.points
            else:
                self.state += (destination_piece.worth - destination_piece.points)
                self.state += destination_piece.points

            #  Game Ended
            if destination_piece.name == "king":
                return True
        
        self.cells[drow][dcol].piece = piece
        self.evaluate_worths()
        return False

    def evaluate_worths(self):
        self.max_player.possible_moves = {}
        self.min_player.possible_moves = {}

        for row in range(8):
            for col in range(8):
                cell = self.cells[row][col]
                piece = cell.piece
                if piece is None:
                    continue

                #  Reset
                piece.worth = piece.points
                piece.possible_moves = []

                #  Caculate ranges and possible moves
                if piece.name == "queen":
                    self.calculate_plus_range(cell)
                    self.calculate_x_range(cell)

                elif piece.name == "rook":
                    self.calculate_plus_range(cell)

                elif piece.name == "bishop":
                    self.calculate_x_range(cell)
                
                elif piece.name == "knight":
                    self.calculate_knight_range(cell)

                elif piece.name == "pawn":
                    self.calculate_pawn_range(cell)
                
                elif piece.name == "king":
                    self.calculate_king_range(cell)
                
                if piece.team == "white":
                    self.max_player.possible_moves.update({cell.position: piece.possible_moves})
                else:
                    self.min_player.possible_moves.update({cell.position: piece.possible_moves})
    
    def check_and_update_worth(self, cell, position):
        row, col = position
        #  Out of board
        if row>7 or col>7 or row<0 or col<0 :
            return True

        piece = cell.piece
        in_range_piece = self.cells[row][col].piece
        if in_range_piece:
            if in_range_piece.team != piece.team:
                in_range_advantage = in_range_piece.worth/2

                piece.worth += in_range_advantage
                if piece.team == "white":
                    self.state += in_range_advantage
                else:
                    self.state -= in_range_advantage

                piece.possible_moves.append(position)    
                # print(f"{piece.name}({piece.team[:1]})[{piece.worth}] has in range {in_range_piece.name}({in_range_piece.team[:1]})[{in_range_piece.worth}]")
                return True
            # print(position, "own piece")
            return True

        if piece.name == "pawn":
            return False

        piece.possible_moves.append(position)
        return False

    def calculate_plus_range(self, cell):
        row, col = cell.position

        up = True
        down = True
        left = True
        right = True
        for i in range(1, 8):
            if up:
                position = (row-i, col)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    up = False
            
            if down:
                position = (row+i, col)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    down = False

            if left:
                position = (row, col-i)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    left = False

            if right:
                position = (row, col+i)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    right = False

    def calculate_x_range(self, cell):
        row, col = cell.position
        
        top_left = True
        top_right = True
        bottom_left = True
        bottom_right = True
        for i in range(1, 8):
            if top_left:
                position = (row-i, col-i)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    top_left = False
            
            if top_right:
                position = (row-i, col+i)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    top_right = False

            if bottom_left:
                position = (row+i, col-i)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    bottom_left = False

            if bottom_right:
                position = (row+i, col+i)
                is_End_or_Blocked = self.check_and_update_worth(cell, position)
                if is_End_or_Blocked:
                    bottom_right = False

    def calculate_knight_range(self, cell):
        row, col = cell.position
        positions = [(row-2, col-1), (row-2, col+1),
                    (row-1, col-2), (row-1, col+2),
                    (row+1, col-2), (row+1, col+2),
                    (row+2, col-1), (row+2, col+1),
                    ]
        for position in positions:
            self.check_and_update_worth(cell, position)

    def calculate_pawn_range(self, cell):
        team = cell.piece.team
        row, col = cell.position
        positions = [(row+1, col-1), (row+1, col+1)] if team == "white" else [(row-1, col-1), (row-1, col+1)]
        for position in positions:
            self.check_and_update_worth(cell, position)
        
        forward = (row+1, col) if team == "white" else (row-1, col)
        fr, fc = forward
        if self.cells[fr][fc].piece is None and 0 <= fr <= 7:
            cell.piece.possible_moves.append(forward)

        #  Initial pawn position double forward move
        double_forward = (row+2, col) if team == "white" else (row-2, col)
        dr, dc = double_forward
        if self.cells[dr][dc].piece is None:
            if team == "white" and row == 1:
                cell.piece.possible_moves.append(double_forward)
            elif team == "black" and row == 6:
                cell.piece.possible_moves.append(double_forward)

    def calculate_king_range(self, cell):
        row, col = cell.position
        positions = [(row+1, col-1), (row+1, col), (row+1, col+1), 
                    (row, col-1), (row, col+1), 
                    (row-1, col-1), (row-1, col), (row-1, col+1),]
        for position in positions:
            self.check_and_update_worth(cell, position)